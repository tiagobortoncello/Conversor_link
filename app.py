import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json

st.title("Gerador de Link Jornal Minas Gerais")

# Input do usuário
input_url = st.text_input("Cole o link original aqui:")

if input_url:
    try:
        # Quebra o link em partes
        parsed_url = urlparse(input_url)
        query_params = parse_qs(parsed_url.query)

        # Pega o parâmetro 'dados' e decodifica JSON
        dados_json = query_params.get("dados", [None])[0]
        if dados_json:
            dados_dict = json.loads(dados_json)

            # Mantém apenas a chave 'dataPublicacaoSelecionada'
            nova_dict = {
                "dataPublicacaoSelecionada": dados_dict.get("dataPublicacaoSelecionada")
            }

            # Codifica de volta para string JSON e URL
            novo_dados = json.dumps(nova_dict)
            novo_query = urlencode({"dados": novo_dados})

            # Monta o novo link
            novo_link = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                novo_query,
                parsed_url.fragment
            ))

            st.success("Link transformado com sucesso!")
            st.code(novo_link, language="text")
        else:
            st.error("O link não contém o parâmetro 'dados'.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
