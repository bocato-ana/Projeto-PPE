import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚖️ Auditoria de Dados: Análise de Viés e Tecnologia")

# 1. Seletor de Métrica Único
tipo_visao = st.radio(
    "📊 Escolha a métrica do gráfico:",
    options=["Quantidade Absoluta", "Porcentagem (Proporcional)"],
    horizontal=True,
    help="A porcentagem mostra a distribuição interna de cada grupo (ex: % de todas as mulheres que usam Python)."
)

if 'data' in st.session_state:
    df_base = st.session_state['data'].copy()
    
    # 2. Filtros Laterais
    st.sidebar.header("Filtros de Auditoria")
    generos_sel = st.sidebar.multiselect("Gênero", options=df_base['Gênero'].unique(), default=df_base['Gênero'].unique())
    cores_sel = st.sidebar.multiselect("Cor/Etnia", options=df_base['Cor/Etnia'].unique(), default=df_base['Cor/Etnia'].unique())

    df_filtrado = df_base[
        (df_base['Gênero'].isin(generos_sel)) & 
        (df_base['Cor/Etnia'].isin(cores_sel))
    ]

    # Ordens Lógicas
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
    ordem_nivel = ['Júnior', 'Pleno', 'Sênior', 'Gestão']

    # --- FUNÇÃO DE CRIAÇÃO DE GRÁFICO (RECALCULADA) ---
    def criar_figura(df, eixo_x, cor_grupo, titulo, ordem_x, paleta):
        if tipo_visao == "Porcentagem (Proporcional)":
            # Agrupa e calcula % sobre o total de cada COR/GÊNERO
            df_contagem = df.groupby([eixo_x, cor_grupo]).size().reset_index(name='n')
            total_por_grupo = df_contagem.groupby(cor_grupo)['n'].transform('sum')
            df_contagem['Percentual (%)'] = (df_contagem['n'] / total_por_grupo) * 100
            
            fig = px.bar(df_contagem, x=eixo_x, y='Percentual (%)', color=cor_grupo,
                         barmode='group', category_orders={eixo_x: ordem_x},
                         color_discrete_sequence=paleta, title=titulo,
                         labels={'Percentual (%)': '% do grupo'})
        else:
            fig = px.histogram(df, x=eixo_x, color=cor_grupo, barmode='group',
                               category_orders={eixo_x: ordem_x},
                               color_discrete_sequence=paleta, title=titulo)
        return fig

    # --- SEÇÃO 1: SALÁRIOS ---
    st.subheader("💰 Distribuição Salarial")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Gênero', "Salário por Gênero", ordem_salario, px.colors.qualitative.Safe), use_container_width=True)
    with c2:
        st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Cor/Etnia', "Salário por Cor/Etnia", ordem_salario, px.colors.qualitative.Bold), use_container_width=True)

    st.divider()

    # --- SEÇÃO 2: TECNOLOGIAS (NOVIDADE) ---
    st.header("🤖 Ferramentas e Tecnologias")
    # Para linguagens, é melhor um gráfico horizontal se houverem muitas
    fig_lang = criar_figura(df_filtrado, 'Linguagem mais usada', 'Gênero', "Linguagem por Gênero", None, px.colors.qualitative.Prism)
    st.plotly_chart(fig_lang, use_container_width=True)

    st.divider()

    # --- SEÇÃO 3: CARREIRA ---
    st.header("📈 Evolução e Progressão")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(criar_figura(df_filtrado, 'Nivel', 'Gênero', "Nível por Gênero", ordem_nivel, px.colors.qualitative.Pastel), use_container_width=True)
    with c4:
        # Gráfico de Linhas Proporcional
        df_line = df_filtrado.groupby(['Nivel', 'Gênero']).size().reset_index(name='qtd')
        if tipo_visao == "Porcentagem (Proporcional)":
            df_line['Métrica'] = (df_line['qtd'] / df_line.groupby('Gênero')['qtd'].transform('sum')) * 100
            y_lab = "Porcentagem (%)"
        else:
            df_line['Métrica'] = df_line['qtd']
            y_lab = "Qtd. Absoluta"
        fig_line = px.line(df_line, x='Nivel', y='Métrica', color='Gênero', markers=True,
                           category_orders={'Nivel': ordem_nivel}, title="Acesso a Cargos de Liderança",
                           labels={'Métrica': y_lab})
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.error("⚠️ Inicie pela Home para carregar os dados.")