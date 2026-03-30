import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise de Viés")

# 1. Seletor de Métrica
tipo_visao = st.radio(
    "📊 Escolha a métrica do gráfico:",
    options=["Quantidade Absoluta", "Porcentagem (Proporcional)"],
    horizontal=True,
    help="A porcentagem ajuda a comparar grupos de tamanhos diferentes (ex: Homens vs Mulheres) de forma justa."
)

if 'data' in st.session_state:
    df_base = st.session_state['data'].copy()
    
    # 2. Filtros
    st.sidebar.header("Filtros de Auditoria")
    generos_sel = st.sidebar.multiselect("Gênero", options=df_base['Gênero'].unique(), default=df_base['Gênero'].unique())
    cores_sel = st.sidebar.multiselect("Cor/Etnia", options=df_base['Cor/Etnia'].unique(), default=df_base['Cor/Etnia'].unique())

    df_filtrado = df_base[
        (df_base['Gênero'].isin(generos_sel)) & 
        (df_base['Cor/Etnia'].isin(cores_sel))
    ]

    # 3. Definição de Ordens e Cores (Roxo/Azul fixos)
    ordem_salario = [
        'Menos de R$ 1.000/mês', 'de R$ 1.001/mês a R$ 2.000/mês', 'de R$ 2.001/mês a R$ 3.000/mês', 
        'de R$ 3.001/mês a R$ 4.000/mês', 'de R$ 4.001/mês a R$ 6.000/mês', 'de R$ 6.001/mês a R$ 8.000/mês',
        'de R$ 8.001/mês a R$ 12.000/mês', 'de R$ 12.001/mês a R$ 16.000/mês', 'de R$ 16.001/mês a R$ 20.000/mês', 
        'de R$ 20.001/mês a R$ 25.000/mês', 'de R$ 25.001/mês a R$ 30.000/mês', 'de R$ 30.001/mês a R$ 40.000/mês',
        'Acima de R$ 40.001/mês'
    ]
    ordem_nivel = ['Júnior', 'Pleno', 'Sênior', 'Gestão']
    
    mapa_cores = {
        'Feminino': '#9D4EDD',   # Roxo
        'Masculino': '#0077B6',  # Azul
        'Prefiro não informar': '#ADB5BD',
        'Outro': '#FF9E00'
    }

    #FUNÇÃO PADRÃO PARA BARRAS
    def criar_figura(df, eixo_x, cor_grupo, titulo, ordem_x, usar_mapa=True):
        if tipo_visao == "Porcentagem (Proporcional)":
            df_contagem = df.groupby([eixo_x, cor_grupo]).size().reset_index(name='n')
            total = df_contagem.groupby(cor_grupo)['n'].transform('sum')
            df_contagem['%'] = (df_contagem['n'] / total.replace(0, 1)) * 100
            
            fig = px.bar(df_contagem, x=eixo_x, y='%', color=cor_grupo,
                         barmode='group', category_orders={eixo_x: ordem_x},
                         color_discrete_map=mapa_cores if usar_mapa else None,
                         title=titulo, labels={'%': 'Porcentagem (%)'})
        else:
            fig = px.histogram(df, x=eixo_x, color=cor_grupo, barmode='group',
                               category_orders={eixo_x: ordem_x},
                               color_discrete_map=mapa_cores if usar_mapa else None,
                               title=titulo)
        return fig

    #EXIBIÇÃO
    st.subheader("💰 Distribuição Salarial")
    st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Gênero', "Salário por Gênero", ordem_salario), use_container_width=True)
    st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Cor/Etnia', "Salário por Cor/Etnia", ordem_salario, usar_mapa=False), use_container_width=True)

    st.divider()
    st.subheader(" Recorte por Idade")
    st.plotly_chart(criar_figura(df_filtrado, 'Idade', 'Gênero', "Distribuição de Idade por Gênero", None), use_container_width=True)

    st.divider()
    st.subheader("📈 Progressão de Carreira")
    
    # Gráfico de Barras de Nível
    st.plotly_chart(criar_figura(df_filtrado, 'Nivel', 'Gênero', "Nível Hierárquico por Gênero", ordem_nivel), use_container_width=True)

    
    df_line = df_filtrado.groupby(['Nivel', 'Gênero']).size().reset_index(name='qtd')
    if tipo_visao == "Porcentagem (Proporcional)":
        df_line['Métrica'] = (df_line['qtd'] / df_line.groupby('Gênero')['qtd'].transform('sum').replace(0,1)) * 100
        y_label = "Porcentagem (%)"
    else:
        df_line['Métrica'] = df_line['qtd']
        y_label = "Quantidade Absoluta"

    fig_linhas = px.line(
        df_line, x='Nivel', y='Métrica', color='Gênero', markers=True,
        category_orders={'Nivel': ordem_nivel},
        color_discrete_map=mapa_cores,
        title="Tendência de Acesso a Cargos de Liderança",
        labels={'Métrica': y_label}
    )
    st.plotly_chart(fig_linhas, use_container_width=True)

else:
    st.error("⚠️ Dados não carregados.")