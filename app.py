import streamlit as st
from urllib.parse import urlparse, parse_qs, quote
import json

st.title("Gerador de Link Jornal Minas Gerais")

input_url = st.text_input("Cole o link original aqui:")

if input_url:
    try:
        parsed_url = urlparse(input_url)
        query_params = parse_qs(parsed_url.query)

        dados_json = query_params.get("dados", [None])[0]
        if dados_json:
            dados_dict = json.loads(dados_json)
            nova_dict = {
                "dataPublicacaoSelecionada": dados_dict.get("dataPublicacaoSelecionada")
            }

            # Codifica o JSON exatamente no formato desejado
            novo_dados = quote(json.dumps(nova_dict, separators=(',', ':')))
            novo_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?dados={novo_dados}"

            st.success("Link transformado com sucesso!")

            # Caixa maior para o link
            st.text_area("Link transformado (copie manualmente):", value=novo_link, height=100)

            # Botão apenas visual para chamar atenção
            st.markdown("""
                <button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;">
                📋 Copiar link
                </button>
                <p style="font-size:14px;color:gray;">Clique na caixa acima e use Ctrl+C / Cmd+C para copiar.</p>
            """, unsafe_allow_html=True)

        else:
            st.error("O link não contém o parâmetro 'dados'.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
