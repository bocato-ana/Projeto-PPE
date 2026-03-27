import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Título da Página (já usando o layout wide da app.py)
st.title("⚖️ Análise de Viés e Disparidade Salarial")

# 2. Carregar os dados "limpos" da sessão
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # 3. Configurar os Filtros na Barra Lateral (Sidebar)
    st.sidebar.header("Filtros de Auditoria")
    
    # Filtro de Gênero
    lista_generos = df['Gênero'].unique().tolist()
    generos_sel = st.sidebar.multiselect("Selecione o Gênero", options=lista_generos, default=lista_generos)
    
    # Filtro de Cor/Etnia
    lista_cores = df['Cor/Etnia'].unique().tolist()
    cores_sel = st.sidebar.multiselect("Selecione Cor/Etnia", options=lista_cores, default=lista_cores)

    # Aplicando os filtros ao DataFrame
    df_filtrado = df[
        (df['Gênero'].isin(generos_sel)) & 
        (df['Cor/Etnia'].isin(cores_sel))
    ]

    
    
    # Definindo a ordem salarial para o gráfico não ficar bagunçado (ordem alfabética)
    ordem_salario = [
        'Menos de R$ 1.000/mês', 
        'de R$ 1.001/mês a R$ 2.000/mês', 
        'de R$ 2.001/mês a R$ 3.000/mês',
        'de R$ 3.001/mês a R$ 4.000/mês',
        'de R$ 4.001/mês a R$ 6.000/mês',
        'de R$ 6.001/mês a R$ 8.000/mês',
        'de R$ 8.001/mês a R$ 12.000/mês',
        'de R$ 12.001/mês a R$ 16.000/mês',
        'de R$ 16.001/mês a R$ 20.000/mês',
        'de R$ 20.001/mês a R$ 25.000/mês',
        'de R$ 25.001/mês a R$ 30.000/mês',
        'de R$ 30.001/mês a R$ 40.000/mês',
        'Acima de R$ 40.001/mês'
    ]
    # Layout em Colunas para os gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Salário (mês) por Gênero")
        fig_gen = px.histogram(
            df_filtrado, 
            x='Salário', 
            color='Gênero', 
            barmode='group',
            category_orders={'Salário': ordem_salario},
            color_discrete_sequence=px.colors.qualitative.Safe 
        )
        st.plotly_chart(fig_gen, use_container_width=True)

    with col2:
        st.subheader("Salário(mês) por Cor/Etnia")
        fig_raca = px.histogram(
            df_filtrado, 
            x='Salário', 
            color='Cor/Etnia', 
            barmode='group',
            category_orders={'Salário': ordem_salario},
    
            color_discrete_sequence=px.colors.qualitative.Bold 
        )
        st.plotly_chart(fig_raca, use_container_width=True)

    
    st.divider()
    st.subheader("Distribuição por Faixa Etária")
    fig_idade = px.histogram(
        df_filtrado, 
        x='Salário', 
        color='Idade', 
        barmode='group',
        category_orders={'Salário': ordem_salario},
        height=500 # Aumentando a altura para este gráfico
    )
    st.plotly_chart(fig_idade, use_container_width=True)

    st.header("📊 Evolução na Carreira")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nível por Gênero")
        # Definindo a ordem lógica dos níveis
        ordem_nivel = ['Júnior', 'Pleno', 'Sênior', 'Gestão'] 
        
        fig_nivel = px.histogram(
            df, 
            x='Nivel', 
            color='Gênero', 
            barmode='group',
            category_orders={'Nivel': ordem_nivel},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_nivel, use_container_width=True)

    ordem_experiencia = [
    'Não tive experinência na área de TI/Engenharia de Software antes de começar a trabalhar na área de dados',
    'Menos de 1 ano',
    'de 1 a 2 anos',
    'de 2 a 3 anos',
    'de 3 a 4 anos',
    'de 4 a 5 anos',
    'de 5 a 6 anos',
    'de 7 a 10 anos',
    'Mais de 10 anos'
]
    with col2:
        st.subheader("Tempo de Experiência por Gênero")
    
        fig_exp = px.histogram(
            df, 
            x='Tempo de experiencia', 
            color='Gênero', 
            barmode='group',
            category_orders={'Tempo de experiencia': ordem_experiencia},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_exp, use_container_width=True, height=800)

    st.divider()
    st.header("🤖 Ferramentas e Tecnologias")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Linguagem Mais Usada")
        
        fig_pizza_lang = px.pie(
            df, 
            names='Linguagem mais usada', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pizza_lang, use_container_width=True)


  
    st.divider()
    st.subheader("📈 Tendência de Nível (Visualização em Linhas)")
    
    
    # Agrupando os dados para o gráfico de linhas funcionar
    df_linhas = df.groupby(['Nivel', 'Gênero']).size().reset_index(name='Quantidade')
    
    fig_linhas = px.line(
        df_linhas, 
        x='Nivel', 
        y='Quantidade', 
        color='Gênero',
        markers=True,
        category_orders={'Nivel': ordem_nivel},
        title="Fluxo de Profissionais por Nível Hierárquico"
    )
    st.plotly_chart(fig_linhas, use_container_width=True)

else:
    st.error("⚠️ Dados não carregados. Por favor, inicie pela Página Inicial.")