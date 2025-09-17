import streamlit as st
from datetime import datetime, timedelta
import json

st.title("Gerador de Link Jornal Minas Gerais (Sem Domingos)")

# Inicializa a data
if "data" not in st.session_state:
    st.session_state.data = datetime.today().date()

# Funções para alterar a data
def dia_anterior():
    st.session_state.data -= timedelta(days=1)
    if st.session_state.data.weekday() == 6:  # domingo
        st.session_state.data -= timedelta(days=1)

def dia_posterior():
    st.session_state.data += timedelta(days=1)
    if st.session_state.data.weekday() == 6:  # domingo
        st.session_state.data += timedelta(days=1)

# Input de data com calendário
data_selecionada = st.date_input(
    "Selecione a data de publicação:",
    st.session_state.data
)

# Atualiza o estado com a data escolhida
st.session_state.data = data_selecionada

# Validação para não permitir domingos
if st.session_state.data.weekday() == 6:  # 6 = domingo
    st.error("Domingos não são permitidos! Escolha outra data.")
else:
    # Botões para avançar ou voltar um dia
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("⬅️ Dia Anterior"):
            dia_anterior()
    with col2:
        if st.button("➡️ Próximo Dia"):
            dia_posterior()

    # Formata a data no padrão do link (YYYY-MM-DD)
    data_formatada_link = st.session_state.data.strftime("%Y-%m-%d")
    dados_dict = {"dataPublicacaoSelecionada": f"{data_formatada_link}T06:00:00.000Z"}

    # Serializa JSON sem espaços e codifica { } e "
    json_str = json.dumps(dados_dict, separators=(',', ':'))
    novo_dados = json_str.replace("{", "%7B").replace("}", "%7D").replace('"', "%22")

    # Monta o link final
    novo_link = f"https://www.jornalminasgerais.mg.gov.br/edicao-do-dia?dados={novo_dados}"

    # Mostra a data escolhida em formato dd/mm/aaaa
    st.markdown(f"**Data escolhida (dd/mm/aaaa):** {st.session_state.data.strftime('%d/%m/%Y')}")

    st.success("Link gerado com sucesso!")
    st.text_area("Link:", value=novo_link, height=100)

    # Botão para copiar
    if st.button("📋 Copiar Link"):
        st.markdown(f"""
        <script>
        navigator.clipboard.writeText("{novo_link}");
        alert("Link copiado para a área de transferência!");
        </script>
        """, unsafe_allow_html=True)
