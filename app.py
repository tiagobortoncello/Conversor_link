import streamlit as st
from urllib.parse import urlparse, parse_qs
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

            # Mantém apenas 'dataPublicacaoSelecionada'
            nova_dict = {
                "dataPublicacaoSelecionada": dados_dict.get("dataPublicacaoSelecionada")
            }

            # Serializa JSON sem espaços
            json_str = json.dumps(nova_dict, separators=(',', ':'))

            # Codifica { } e " corretamente
            novo_dados = json_str.replace("{", "%7B").replace("}", "%7D").replace('"', "%22")

            # Monta link final
            novo_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?dados={novo_dados}"

            st.success("Link transformado com sucesso!")

            # Caixa de texto com o link
            st.text_area("Link transformado:", value=novo_link, height=100)

            # Botão para copiar
            if st.button("📋 Copiar Link"):
                # Copia para a área de transferência usando JS
                st.markdown(f"""
                <script>
                navigator.clipboard.writeText("{novo_link}");
                alert("Link copiado para a área de transferência!");
                </script>
                """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-size:14px;color:gray;">
            ⚠️ Clique no botão acima para copiar o link automaticamente.
            </p>
            """, unsafe_allow_html=True)

        else:
            st.error("O link não contém o parâmetro 'dados'.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
