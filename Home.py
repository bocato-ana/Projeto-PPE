import streamlit as st
import pandas as pd
import plotly.express as px

st.title('📔Estudo - State of Data Brazil 2024-2025')
st.subheader('🔎Sobre o Projeto:')
st.markdown("""
**Instituição:** Universidade Federal de São Paulo (Unifesp) - São José dos Campos  
**Curso:** Bacharelado em Ciência e Tecnologia (BCT)   
**Orientadora:** Profa. Dra. Lilian Berton  
**Discente:** Ana Luiza Bocato
---
""")
st.write("""
**Este dashboard é a primeira etapa da análise de dados**. 

Foi o dataset **State of Data Brazil 2024**, o maior mapeamento do mercado de dados no país, para auditar possíveis disparidades.

**Neste sistema, você encontrará:**
1.  **Exploração de Dados Brutos:** Uma visão transparente da tabela utilizada.
2.  **Análise de Viés:** Gráficos interativos que cruzam faixas salariais com indicadores demográficos (Gênero, Raça e Idade).
         
Se encontram na URL [Kaggle - |State of Data Brazil](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)
""")

dicionario_colunas = {
        '1.a.1_faixa_idade': 'Idade',
        '1.b_genero': 'Gênero',
        '1.c_cor/raca/etnia': 'Cor/Etnia',
        '2.g_nivel': 'Nivel',
        '2.h_faixa_salarial': 'Salário',
        '2.j_tempo_de_experiencia_em_ti': 'Tempo de experiencia',
        '4.e_linguagem_mais_usada': 'Linguagem mais usada',
        '4.m_usa_chatgpt_ou_copilot_no_trabalho': 'Modelos de IA'
    }

with st.sidebar:
    st.title('🔗Links Úteis:')
    st.write('[State of Data Brazil](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)')
    st.write('[Link Repositório GitHub](https://github.com/bocato-ana/Projeto-PPE.git)')


if 'data' not in st.session_state:
    df_data = pd.read_csv('data_2024.csv')
    st.session_state['data'] = df_data
    
    # Filtra apenas as colunas que existem no dicionário para evitar erros
    colunas_existentes = [col for col in dicionario_colunas.keys() if col in df_data.columns]
    df_filtrado = df_data[colunas_existentes].copy()
    
    # Renomeia (usando df_filtrado em vez do df_raw que não existia)
    df_limpo = df_filtrado.rename(columns=dicionario_colunas)

    # Salva o DataFrame já bonitinho na sessão
    st.session_state['data'] = df_limpo

