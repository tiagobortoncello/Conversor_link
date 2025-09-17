import streamlit as st
from urllib.parse import urlparse, parse_qs, quote
import json
import streamlit.components.v1 as components

st.title("Gerador de Link Jornal Minas Gerais")

input_url = st.text_input("Cole o link original aqui:")

if input_url:
    try:
        parsed_url = urlparse(input_url)
        query_params = parse_qs(parsed_url.query)

        dados_json = query_params.get("dados", [None])[0]
        if dados_json:
            dados_dict = json.loads(dados_json)

            # Mantém apenas 'dataPublicacaoSelecionada'
            nova_dict = {
                "dataPublicacaoSelecionada": dados_dict.get("dataPublicacaoSelecionada")
            }

            # Codifica JSON exatamente no formato desejado
            json_str = json.dumps(nova_dict, separators=(',', ':'))  # remove espaços
            novo_dados = quote(json_str, safe='"')  # mantém aspas

            # Monta o link final
            novo_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?dados={novo_dados}"

            st.success("Link transformado com sucesso!")

            # Caixa de texto grande
            st.text_area("Link transformado:", value=novo_link, height=100)

            # Botão de copiar funcional usando JavaScript
            copy_button_html = f"""
            <button onclick="navigator.clipboard.writeText('{novo_link}')" 
                style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;">
                📋 Copiar link
            </button>
            <p style="font-size:14px;color:gray;">Clique no botão para copiar automaticamente.</p>
            """
            components.html(copy_button_html)

        else:
            st.error("O link não contém o parâmetro 'dados'.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
