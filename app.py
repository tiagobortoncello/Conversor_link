import streamlit as st
from datetime import datetime, timedelta
import json

st.title("Gerador de Link Jornal Minas Gerais")

# Estado para armazenar a data atual
if "data" not in st.session_state:
    st.session_state.data = datetime.today().date()

# Funções para alterar a data
def dia_anterior():
    st.session_state.data -= timedelta(days=1)

def dia_posterior():
    st.session_state.data += timedelta(days=1)

# Selecionar data manualmente
st.session_state.data = st.date_input("Selecione a data de publicação:", st.session_state.data)

# Botões para avançar ou voltar um dia
col1, col2 = st.columns([1,1])
with col1:
    if st.button("⬅️ Dia Anterior"):
        dia_anterior()
with col2:
    if st.button("➡️ Próximo Dia"):
        dia_posterior()

# Formata a data no padrão do link
data_formatada = st.session_state.data.strftime("%Y-%m-%d")
dados_dict = {"dataPublicacaoSelecionada": f"{data_formatada}T06:00:00.000Z"}

# Serializa JSON sem espaços e codifica { } e "
json_str = json.dumps(dados_dict, separators=(',', ':'))
novo_dados = json_str.replace("{", "%7B").replace("}", "%7D").replace('"', "%22")

# Monta o link final
novo_link = f"https://www.jornalminasgerais.mg.gov.br/edicao-do-dia?dados={novo_dados}"

st.success("Link gerado com sucesso!")

# Caixa de texto com o link
st.text_area("Link:", value=novo_link, height=100)

# Botão para copiar
if st.button("📋 Copiar Link"):
    st.markdown(f"""
    <script>
    navigator.clipboard.writeText("{novo_link}");
    alert("Link copiado para a área de transferência!");
    </script>
    """, unsafe_allow_html=True)
