import streamlit as st

st.title("📊 Resumo da Auditoria Algorítmica: Viés de Gênero")
st.subheader('Estudo realizado através de regressão lógica e árvore de decisão')

st.write("""Todo o estudo se encontra no repositório do [GitHub - notebooks](https://github.com/bocato-ana/Projeto-PPE/blob/main/notebooks/treino_modelo.ipynb)""")

import streamlit as st



st.markdown("""
O objetivo deste estudo foi verificar se modelos de Inteligência Artificial, treinados com dados reais do mercado de tecnologia brasileiro (**State of Data**), replicam desigualdades históricas de gênero ao realizar previsões salariais.

---

### 🌳 1. Árvore de Decisão: O "Mapa do Privilégio"
A Árvore de Decisão foi utilizada para visualizar as regras lógicas que a IA cria para classificar um salário.

* **Funcionamento:** O modelo cria "nós" de decisão. Em nosso estudo, o **Nível (Sênior/Gestão)** dominou o topo (nó raiz), mas o **Gênero** apareceu logo em seguida como um divisor estatístico determinante.
* **O Estudo de Acurácia:** Descobrimos que a IA tem uma acurácia maior para **mulheres (~37%)** do que para **homens (~29%)**.
* **Interpretação Crítica:** Isso **não** significa que a IA é "melhor" com mulheres. Na verdade, indica que os salários femininos são mais **previsíveis e limitados** a faixas baixas. Os homens possuem trajetórias mais variadas, o que "desafia" a padronização do modelo.
* **Matrizes de Confusão:** Quando a IA erra o salário de uma mulher, ela tende a errar **"para baixo"** (subestimando), enquanto para homens os erros são mais dispersos ou para faixas superiores.
* **O Teste Inverso:** Provamos que a IA consegue deduzir o gênero de um profissional com alta precisão apenas analisando seu salário e nível, confirmando que as faixas salariais **não são neutras**.

---

### 📈 2. Regressão Logística: Os "Pesos da Corda"
Enquanto a árvore mostra o caminho, a Regressão Logística revelou a **intensidade matemática** de cada variável através de coeficientes.

* **Funcionamento:** Cada atributo "puxa" a probabilidade do salário para faixas mais altas ou mais baixas.
* **Pesos Encontrados:**
    * **Nível Profissional (Peso ~2.11):** O fator principal. Quanto maior o cargo, menor a chance de salários baixos (validação de mérito/hierarquia).
    * **Gênero (Peso ~-0.26):** Embora menor que o nível, o peso é estatisticamente **significativo**. O sinal negativo indica que ser mulher (ou "Outro") atua como um **redutor matemático** na probabilidade de alcançar as faixas salariais mais altas.
* **Veredito:** O gênero não é um ruído; é uma variável de "ajuste fino" que o algoritmo usa para alinhar a previsão ao preconceito contido nos dados históricos.

---

### 🔍 3. Dados Omissos: A Hipótese de Omissão
Investigamos o perfil de quem escolheu a opção **"Prefiro não Informar/ Outros"** quanto ao gênero.

* **Achado Estatístico:** O perfil salarial deste grupo é muito superior à média das mulheres, aproximando-se do topo da pirâmide salarial masculina.
* **Conclusão:** Isso corrobora a suspeita de que **homens em cargos de alta gestão** tendem a omitir dados demográficos mais do que outros grupos. Para a IA, isso mascara parte do privilégio masculino, sugerindo que o viés real pode ser ainda **mais profundo** do que o detectado pelo modelo.

""")