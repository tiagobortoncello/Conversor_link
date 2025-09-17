import streamlit as st
from datetime import datetime, timedelta, date
import json

st.title("Gerador de Link Jornal Minas Gerais")

# Define limites do calendário
min_data = date(1835, 1, 1)
max_data = datetime.today().date()

# Inicializa a data, garantindo que esteja dentro do intervalo
if "data" not in st.session_state:
    data_inicial = datetime.today().date()
    if data_inicial < min_data:
        data_inicial = min_data
    elif data_inicial > max_data:
        data_inicial = max_data
    st.session_state.data = data_inicial

# Funções para avançar, voltar e voltar para hoje (pulando domingos)
def dia_anterior():
    st.session_state.data -= timedelta(days=1)
    if st.session_state.data.weekday() == 6:  # domingo
        st.session_state.data -= timedelta(days=1)

def dia_posterior():
    st.session_state.data += timedelta(days=1)
    if st.session_state.data.weekday() == 6:  # domingo
        st.session_state.data += timedelta(days=1)

def ir_hoje():
    hoje = datetime.today().date()
    if hoje.weekday() == 6:  # se hoje for domingo, volta para sábado
        hoje -= timedelta(days=1)
    st.session_state.data = hoje

# Input de data com calendário e limites
data_selecionada = st.date_input(
    "Selecione a data de publicação:",
    st.session_state.data,
    min_value=min_data,
    max_value=max_data
)
st.session_state.data = data_selecionada

# Botões para avançar, voltar e Hoje (habilitados/desabilitados conforme limite)
col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.session_state.data > min_data:
        if st.button("⬅️ Dia Anterior"):
            dia_anterior()
    else:
        st.button("⬅️ Dia Anterior", disabled=True)

with col2:
    if st.button("📅 Hoje"):
        ir_hoje()

with col3:
    if st.session_state.data < max_data:
        if st.button("➡️ Próximo Dia"):
            dia_posterior()
    else:
        st.button("➡️ Próximo Dia", disabled=True)

# Validação para domingos
if st.session_state.data.weekday() == 6:  # domingo
    st.error("Domingos não são permitidos! Escolha outra data.")
else:
    # Botão para gerar link
    if st.button("📝 Gerar link"):
        # Formata a data no padrão do link (YYYY-MM-DD)
        data_formatada_link = st.session_state.data.strftime("%Y-%m-%d")
        dados_dict = {"dataPublicacaoSelecionada": f"{data_formatada_link}T06:00:00.000Z"}

        # Serializa JSON sem espaços e codifica { } e "
        json_str = json.dumps(dados_dict, separators=(',', ':'))
        novo_dados = json_str.replace("{", "%7B").replace("}", "%7D").replace('"', "%22")

        # Monta o link final
        novo_link = f"https://www.jornalminasgerais.mg.gov.br/edicao-do-dia?dados={novo_dados}"

        # Mostra a data escolhida em formato dd/mm/aaaa
        st.markdown(f"**Data escolhida:** {st.session_state.data.strftime('%d/%m/%Y')}")

        st.success("Link gerado com sucesso!")
        st.text_area("Link:", value=novo_link, height=100)
