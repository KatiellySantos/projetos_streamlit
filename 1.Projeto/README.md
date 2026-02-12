# 📊 Painel de Desenvolvimento Econômico e Turístico

Dashboard interativo desenvolvido com Streamlit, voltado para análise de indicadores econômicos e turísticos do Brasil, com geração automática de Relatório em PDF.

O projeto apresenta KPIs, gráficos interativos, mapas geográficos e um relatório estruturado com análises dinâmicas a partir dos dados filtrados.

🚀 Tecnologias Utilizadas

Python 3.x

Streamlit

Pandas

Plotly

ReportLab

Kaleido (exportação de gráficos para imagem)

📂 Estrutura do Projeto

📁 projeto
│-- app.py
│-- planilha.xlsx
│-- mapa.geojson
│-- IBGE.PNG
│-- logo.png
│-- requirements.txt (recomendado)

📈 Funcionalidades
🔹 1. Filtros Dinâmicos

A barra lateral permite filtrar os dados por:

Estado

Município

Região Turística

Todos os gráficos e indicadores são atualizados automaticamente conforme os filtros selecionados.

🔹 2. KPIs (Indicadores Principais)

O sistema calcula automaticamente:

Total de Empregos

Total de Estabelecimentos

Visitas Nacionais

Visitas Internacionais

Arrecadação Total

Esses valores são exibidos no topo do dashboard com formatação personalizada.

🔹 3. Indicadores do Turismo

Gráficos disponíveis:

📊 Empregos por Estado

📊 Estabelecimentos por Estado

📊 Comparação entre Visitas Nacionais e Internacionais

🗺️ Mapa de Visitas por Município

Os mapas utilizam choropleth_mapbox com base no arquivo mapa.geojson.

🔹 4. Indicadores de Arrecadação

📈 Evolução da arrecadação por Estado

🗺️ Mapa de arrecadação por Município

Todos os gráficos possuem:

Hover customizado

Formatação monetária brasileira

Layout visual padronizado

🔹 5. Geração de Relatório em PDF

O sistema gera automaticamente um relatório completo contendo:

Título institucional

Data de geração

Introdução explicativa

KPIs organizados em tabela

Gráficos exportados em imagem

Texto analítico automático por estado

Assinatura visual com logo

O PDF é gerado com ReportLab e disponibilizado para download diretamente pelo navegador.

🧠 Como o Código Está Organizado
1️⃣ Configuração Inicial

st.set_page_config() define título, layout e ícone.

Leitura da planilha com pandas.read_excel().

2️⃣ Filtros

Utiliza st.sidebar.multiselect() para aplicar filtros dinâmicos.
O dataframe é filtrado com:

df_filtrado = df[
    (df["Estado"].isin(se_estado)) &
    (df["Município"].isin(se_municipio)) &
    (df["Região Turística"].isin(se_turismo))
]

3️⃣ Cálculo de KPIs

Função dedicada:

def calcula_kpis(df):

Responsável por somar os principais indicadores.

4️⃣ Visualizações

Gráficos criados com:

px.bar()

px.line()

px.choropleth_mapbox()

Com personalização de:

cores

hover

layout

transparência

ordenação

5️⃣ Relatório PDF

Fluxo do PDF:

Criação do objeto SimpleDocTemplate

Construção da lista story

Inserção de:

Parágrafos

Tabelas

Imagens dos gráficos

Exportação do arquivo temporário

Botão de download no Streamlit

Gráficos são convertidos para imagem usando:

fig.write_image(tmp.name, scale=2)

▶️ Como Executar o Projeto
1️⃣ Criar ambiente virtual (opcional, recomendado)

python -m venv venv

Ativar:

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate

2️⃣ Instalar dependências

pip install streamlit pandas plotly reportlab kaleido openpyxl

3️⃣ Executar aplicação

streamlit run app.py

📊 Base de Dados

Os dados utilizados são provenientes do:

Mapa do Turismo Brasileiro (ano-base 2018)

Arquivo esperado:

planilha.xlsx

🎨 Personalizações Visuais

O dashboard utiliza:

CSS customizado via st.markdown()

Layout em abas (st.tabs)

Sidebar fixa

Fundo com degradê

Componentes estilizados manualmente

📌 Possíveis Melhorias Futuras


Inclusão de filtros por ano

Adição de séries temporais reais

Integração com API oficial do IBGE

Autenticação de usuários

Exportação também em Excel

👨‍💻 Autor

Projeto desenvolvido para fins de análise de dados e visualização interativa com geração automatizada de relatório institucional.