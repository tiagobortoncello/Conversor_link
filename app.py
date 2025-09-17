import streamlit as st
from urllib.parse import urlparse, parse_qs, urlunparse, quote
import json

st.title("Gerador de Link Jornal Minas Gerais")

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

            # Mantém apenas 'dataPublicacaoSelecionada'
            nova_dict = {
                "dataPublicacaoSelecionada": dados_dict.get("dataPublicacaoSelecionada")
            }

            # Codifica o JSON manualmente para manter o formato desejado
            novo_dados = quote(json.dumps(nova_dict, separators=(',', ':')))

            # Monta o novo link
            novo_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?dados={novo_dados}"

            st.success("Link transformado com sucesso!")
            st.text_area("Link transformado:", value=novo_link, height=100)

            # Botão de copiar
            if st.button("📋 Copiar link"):
                st.experimental_set_clipboard(novo_link)
                st.success("Link copiado para a área de transferência!")

        else:
            st.error("O link não contém o parâmetro 'dados'.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
