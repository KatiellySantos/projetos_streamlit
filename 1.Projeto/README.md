# Painel de Desenvolvimento Econômico e Turístico

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Pandas](https://img.shields.io/badge/Pandas-Análise%20de%20Dados-blue)
![Plotly](https://img.shields.io/badge/Plotly-Gráficos%20Interativos-green)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-orange)

### 📖 Sobre o Projeto

Este projeto foi desenvolvido para analisar indicadores econômicos e turísticos dos municípios brasileiros utilizando dados provenientes do Mapa do Turismo Brasileiro.

A aplicação reúne informações relacionadas à geração de empregos, estabelecimentos turísticos, fluxo de visitantes e arrecadação, transformando os dados em gráficos, mapas interativos e relatórios automatizados.

Além da visualização dos indicadores, o sistema permite a geração de relatórios em PDF contendo análises consolidadas, gráficos e estatísticas dos dados selecionados.

Dessa forma, o projeto facilita a exploração dos dados e auxilia na interpretação de informações relevantes para estudos econômicos, turísticos e planejamento regional.

### 🎯 Objetivo

Fornecer uma ferramenta que permita visualizar e analisar indicadores econômicos e turísticos de forma simples e intuitiva.

Entre os objetivos do projeto estão:

- Centralizar indicadores turísticos em uma única plataforma.
- Facilitar análises por estado, município e região turística.
- Permitir comparações entre localidades.
- Gerar relatórios automatizados.
- Transformar dados em informações visuais de fácil interpretação.

### 🏗️ Estrutura da Solução

O projeto é composto por uma aplicação principal responsável pela leitura, processamento e apresentação dos dados.

**📊 app.py**

Responsável por toda a lógica da aplicação.

Principais atividades:

- Leitura da base de dados em Excel.
- Aplicação de filtros dinâmicos.
- Cálculo de indicadores econômicos e turísticos.
- Construção de gráficos interativos.
- Exibição de mapas geográficos.
- Geração de relatórios em PDF.
- Personalização visual do dashboard.

Esse módulo funciona como a camada de análise e visualização do projeto.

### 🔄 Fluxo do Projeto

```text
Base de Dados (Excel)
          │
          ▼
      app.py
          │
          ▼
Processamento dos Dados
          │
          ▼
Indicadores e Gráficos
          │
          ▼
Dashboard Interativo
          │
          ▼
Relatórios PDF
```

### 📊 Recursos Disponíveis

**Indicadores**

- Total de empregos.
- Total de estabelecimentos turísticos.
- Total de visitas nacionais.
- Total de visitas internacionais.
- Valor total arrecadado.

**Indicadores do Turismo**

- Quantidade de empregos por estado.
- Quantidade de estabelecimentos turísticos por estado.
- Comparação entre visitas nacionais e internacionais.
- Distribuição geográfica das visitas.

**Indicadores de Arrecadação**

- Arrecadação turística por estado.
- Distribuição geográfica da arrecadação por município.

**Visualização Geográfica**

- Mapas interativos dos municípios.
- Exibição de indicadores diretamente no mapa.
- Navegação baseada nos códigos oficiais dos municípios.

**Relatórios**

- Exportação em PDF.
- Indicadores consolidados.
- Gráficos analíticos.
- Estatísticas por estado.
- Informações de arrecadação.
- Resumos automáticos dos resultados.

## 🛠️ Tecnologias Utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- ReportLab
- GeoJSON
- Matplotlib

### 📂 Estrutura do Projeto

```text
.
├── app.py
├── planilha.xlsx
├── mapa.json
├── logo.png
├── IBGE.png
└── README.md
```

### Arquivos

| Arquivo | Descrição |
|----------|----------|
| app.py | Aplicação principal do dashboard |
| planilha.xlsx | Base de dados utilizada nas análises |
| mapa.json | Dados geográficos utilizados nos mapas |
| logo.png | Logotipo da aplicação |
| IBGE.png | Logotipo utilizado nos relatórios |
| README.md | Documentação do projeto |

### ▶️ Como Executar

**Instalar dependências**

```bash
pip install streamlit pandas plotly reportlab matplotlib openpyxl kaleido
```

**Executar a aplicação**

```bash
streamlit run app.py
```

Após iniciar, o Streamlit abrirá automaticamente no navegador.

## 👨‍💻 Autor

Projeto desenvolvido para fins de análise de dados, visualização de indicadores econômicos e turísticos e geração automatizada de relatórios utilizando Python e Streamlit.

### 📜 Licença
Este projeto está disponível para fins educacionais e de estudo.

As estimativas populacionais utilizadas no projeto são públicas e podem ser consultadas diretamente no portal do instituto.
