import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bias Analysis")

# 1. Seletor de Métrica (Traduzido)
tipo_visao = st.radio(
    "📊 Choose chart metric:",
    options=["Absolute Quantity", "Percentage (Proportional)"],
    horizontal=True,
    help="Percentage helps to fairly compare groups of different sizes (e.g., Male vs Female)."
)

if 'data' in st.session_state:
    df_base = st.session_state['data'].copy()
    
    # --- BLOCO DE TRADUÇÃO DOS DADOS ---
    # Traduzindo os nomes das colunas
    df_base.rename(columns={
        'Gênero': 'Gender', 
        'Cor/Etnia': 'Race/Ethnicity', 
        'Salário': 'Salary', 
        'Idade': 'Age', 
        'Nivel': 'Level'
    }, inplace=True)
    
    # Dicionários de tradução dos valores
    dict_salario = {
        'Menos de R$ 1.000/mês': 'Less than R$ 1,000/month',
        'de R$ 1.001/mês a R$ 2.000/mês': 'R$ 1,001 to R$ 2,000/month',
        'de R$ 2.001/mês a R$ 3.000/mês': 'R$ 2,001 to R$ 3,000/month',
        'de R$ 3.001/mês a R$ 4.000/mês': 'R$ 3,001 to R$ 4,000/month',
        'de R$ 4.001/mês a R$ 6.000/mês': 'R$ 4,001 to R$ 6,000/month',
        'de R$ 6.001/mês a R$ 8.000/mês': 'R$ 6,001 to R$ 8,000/month',
        'de R$ 8.001/mês a R$ 12.000/mês': 'R$ 8,001 to R$ 12,000/month'
    }

    dict_nivel = {
        'Júnior': 'Junior',
        'Pleno': 'Mid-level',
        'Sênior': 'Senior',
        'Gestão': 'Management'
    }

    dict_genero = {
        'Feminino': 'Female',
        'Masculino': 'Male',
        'Prefiro não informar': 'Prefer not to say',
        'Outro': 'Other'
    }
    
    # Aplicando a tradução dentro do DataFrame
    df_base['Salary'] = df_base['Salary'].replace(dict_salario)
    df_base['Level'] = df_base['Level'].replace(dict_nivel)
    df_base['Gender'] = df_base['Gender'].replace(dict_genero)
    # -----------------------------------

    # 2. Filtros Laterais (Agora puxam os valores já em inglês)
    st.sidebar.header("Audit Filters")
    generos_sel = st.sidebar.multiselect("Gender", options=df_base['Gender'].unique(), default=df_base['Gender'].unique())
    cores_sel = st.sidebar.multiselect("Race/Ethnicity", options=df_base['Race/Ethnicity'].unique(), default=df_base['Race/Ethnicity'].unique())

    df_filtrado = df_base[
        (df_base['Gender'].isin(generos_sel)) & 
        (df_base['Race/Ethnicity'].isin(cores_sel))
    ]

    # 3. Definição de Ordens e Cores
    ordem_salario_en = list(dict_salario.values())
    ordem_nivel_en = list(dict_nivel.values())
    
    mapa_cores = {
        'Female': '#9D4EDD',   # Roxo
        'Male': '#0077B6',     # Azul
        'Prefer not to say': '#ADB5BD',
        'Other': '#FF9E00'
    }

    # FUNÇÃO PADRÃO PARA BARRAS
    def criar_figura(df, eixo_x, cor_grupo, titulo, ordem_x, usar_mapa=True):
        if tipo_visao == "Percentage (Proportional)":
            df_contagem = df.groupby([eixo_x, cor_grupo]).size().reset_index(name='n')
            total = df_contagem.groupby(cor_grupo)['n'].transform('sum')
            df_contagem['%'] = (df_contagem['n'] / total.replace(0, 1)) * 100
            
            fig = px.bar(df_contagem, x=eixo_x, y='%', color=cor_grupo,
                         barmode='group', category_orders={eixo_x: ordem_x},
                         color_discrete_map=mapa_cores if usar_mapa else None,
                         title=titulo, labels={'%': 'Percentage (%)'})
        else:
            fig = px.histogram(df, x=eixo_x, color=cor_grupo, barmode='group',
                               category_orders={eixo_x: ordem_x},
                               color_discrete_map=mapa_cores if usar_mapa else None,
                               title=titulo)
        return fig

    # EXIBIÇÃO NA TELA PRINCIPAL
    st.subheader("💰 Salary Distribution")
    st.plotly_chart(criar_figura(df_filtrado, 'Salary', 'Gender', "Salary by Gender", ordem_salario_en), use_container_width=True)
    st.plotly_chart(criar_figura(df_filtrado, 'Salary', 'Race/Ethnicity', "Salary by Race/Ethnicity", ordem_salario_en, usar_mapa=False), use_container_width=True)

    st.divider()
    st.subheader("👥 Age Breakdown")
    st.plotly_chart(criar_figura(df_filtrado, 'Age', 'Gender', "Age Distribution by Gender", None), use_container_width=True)

    st.divider()
    st.subheader("📈 Career Progression")
    
    # Gráfico de Barras de Nível
    st.plotly_chart(criar_figura(df_filtrado, 'Level', 'Gender', "Hierarchical Level by Gender", ordem_nivel_en), use_container_width=True)

    # Gráfico de Linha de Liderança
    df_line = df_filtrado.groupby(['Level', 'Gender']).size().reset_index(name='qtd')
    
    if tipo_visao == "Percentage (Proportional)":
        df_line['Metric'] = (df_line['qtd'] / df_line.groupby('Gender')['qtd'].transform('sum').replace(0,1)) * 100
        y_label = "Percentage (%)"
    else:
        df_line['Metric'] = df_line['qtd']
        y_label = "Absolute Quantity"

    fig_linhas = px.line(
        df_line, x='Level', y='Metric', color='Gender', markers=True,
        category_orders={'Level': ordem_nivel_en},
        color_discrete_map=mapa_cores,
        title="Trend of Access to Leadership Roles",
        labels={'Metric': y_label}
    )
    st.plotly_chart(fig_linhas, use_container_width=True)

else:
    st.error("⚠️ Data not loaded.")