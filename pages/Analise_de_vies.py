import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Título e Configuração de Visão
st.title("⚖️ Auditoria de Dados: Análise de Viés")

tipo_visao = st.radio(
    "📊 Escolha a métrica do gráfico:",
    options=["Quantidade Absoluta", "Porcentagem (Proporcional)"],
    horizontal=True,
    help="A porcentagem é calculada sobre o total de cada grupo. Isso permite comparar minorias de forma justa com maiorias."
)

if 'data' in st.session_state:
    df_base = st.session_state['data'].copy()
    
    # 2. Filtros Laterais
    st.sidebar.header("Filtros de Auditoria")
    generos_opcoes = df_base['Gênero'].unique().tolist()
    generos_sel = st.sidebar.multiselect("Filtrar Gênero", options=generos_opcoes, default=generos_opcoes)
    
    cores_opcoes = df_base['Cor/Etnia'].unique().tolist()
    cores_sel = st.sidebar.multiselect("Filtrar Cor/Etnia", options=cores_opcoes, default=cores_opcoes)

    df_filtrado = df_base[
        (df_base['Gênero'].isin(generos_sel)) & 
        (df_base['Cor/Etnia'].isin(cores_sel))
    ]

    # 3. Definição de Ordens Categóricas
    ordem_salario = [
        'Menos de R$ 1.000/mês', 'de R$ 1.001/mês a R$ 2.000/mês', 
        'de R$ 2.001/mês a R$ 3.000/mês', 'de R$ 3.001/mês a R$ 4.000/mês',
        'de R$ 4.001/mês a R$ 6.000/mês', 'de R$ 6.001/mês a R$ 8.000/mês',
        'de R$ 8.001/mês a R$ 12.000/mês', 'de R$ 12.001/mês a R$ 16.000/mês',
        'de R$ 16.001/mês a R$ 20.000/mês', 'de R$ 20.001/mês a R$ 25.000/mês',
        'de R$ 25.001/mês a R$ 30.000/mês', 'de R$ 30.001/mês a R$ 40.000/mês',
        'Acima de R$ 40.001/mês'
    ]
    ordem_nivel = ['Júnior', 'Pleno', 'Sênior', 'Gestão']
    
    # Ordem para idades (State of Data costuma usar faixas)
    ordem_idade = sorted(df_base['Idade'].unique().tolist())

    # Mapa de cores fixas para Gênero (Neutralidade visual)
    mapa_cores = {
        'Feminino': '#9D4EDD',   # Roxo
        'Masculino': '#0077B6',  # Azul
        'Prefiro não informar': '#ADB5BD',
        'Outro': '#FF9E00'
    }

    # --- FUNÇÃO DE CÁLCULO E FORMATAÇÃO ---
    def criar_figura(df, eixo_x, cor_grupo, titulo, ordem_x, usar_mapa=True):
        if tipo_visao == "Porcentagem (Proporcional)":
            df_contagem = df.groupby([eixo_x, cor_grupo]).size().reset_index(name='n')
            total_por_grupo = df_contagem.groupby(cor_grupo)['n'].transform('sum')
            df_contagem['Percentual (%)'] = (df_contagem['n'] / total_por_grupo.replace(0, 1)) * 100
            
            fig = px.bar(df_contagem, x=eixo_x, y='Percentual (%)', color=cor_grupo,
                         barmode='group', category_orders={eixo_x: ordem_x},
                         color_discrete_map=mapa_cores if usar_mapa else None,
                         title=titulo, labels={'Percentual (%)': '% do grupo'})
        else:
            fig = px.histogram(df, x=eixo_x, color=cor_grupo, barmode='group',
                               category_orders={eixo_x: ordem_x},
                               color_discrete_map=mapa_cores if usar_mapa else None,
                               title=titulo)
        
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            margin=dict(l=20, r=20, t=100, b=180),
            bargap=0.4,
            legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="center", x=0.5),
            height=650
        )
        return fig

    # --- EXIBIÇÃO ---
    
    st.subheader("💰 Distribuição Salarial")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Gênero', "Salário por Gênero", ordem_salario), use_container_width=True)
    with c2:
        # Para cor/etnia usamos a paleta padrão pois são muitos grupos para mapear um a um agora
        st.plotly_chart(criar_figura(df_filtrado, 'Salário', 'Cor/Etnia', "Salário por Cor/Etnia", ordem_salario, usar_mapa=False), use_container_width=True)

    st.divider()

    # --- NOVA SEÇÃO: IDADE (PEDIDO DA PROFESSORA) ---
    st.subheader("🎂 Recorte por Idade")
    fig_idade = criar_figura(df_filtrado, 'Idade', 'Gênero', "Distribuição de Idade por Gênero", ordem_idade)
    st.plotly_chart(fig_idade, use_container_width=True)

    st.divider()

    st.subheader("🤖 Ferramentas e Tecnologias")
    fig_lang = criar_figura(df_filtrado, 'Linguagem mais usada', 'Gênero', "Linguagem por Gênero", None)
    st.plotly_chart(fig_lang, use_container_width=True)

    st.divider()
    
    st.subheader("📈 Nível e Progressão")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(criar_figura(df_filtrado, 'Nivel', 'Gênero', "Nível por Gênero", ordem_nivel), use_container_width=True)
    with c4:
        df_line = df_filtrado.groupby(['Nivel', 'Gênero']).size().reset_index(name='qtd')
        if tipo_visao == "Porcentagem (Proporcional)":
            df_line['Métrica'] = (df_line['qtd'] / df_line.groupby('Gênero')['qtd'].transform('sum').replace(0,1)) * 100
            y_lab = "Porcentagem (%)"
        else:
            df_line['Métrica'] = df_line['qtd']
            y_lab = "Qtd. Absoluta"
            
        fig_line = px.line(df_line, x='Nivel', y='Métrica', color='Gênero', markers=True,
                           category_orders={'Nivel': ordem_nivel}, title="Acesso a Cargos de Liderança",
                           color_discrete_map=mapa_cores, labels={'Métrica': y_lab})
        fig_line.update_layout(margin=dict(t=80, b=80))
        st.plotly_chart(fig_line, use_container_width=True)

    if tipo_visao == "Porcentagem (Proporcional)":
        st.info("💡 **Dica:** Algumas porcentagens podem aparecer maior por conta de alguns grupos serem \"menores\"")

else:
    st.error("⚠️ Dados não carregados.")