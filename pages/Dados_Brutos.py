import streamlit as st

st.set_page_config(page_title="Projeto Dados", layout="wide")

st.title('Tabelo de estudo - State of Data Brazil 2024 - 2025')

st.subheader("📋 Visualização dos Dados Selecionados")
# Mostra a tabela ocupando toda a largura disponível
st.dataframe(st.session_state['data'], use_container_width=True, height=5000)

