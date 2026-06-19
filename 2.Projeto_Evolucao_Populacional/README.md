# 📊 Painel de Estimativas Populacionais dos Municípios Brasileiros

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Pandas](https://img.shields.io/badge/Pandas-Análise%20de%20Dados-blue)
![Plotly](https://img.shields.io/badge/Plotly-Gráficos%20Interativos-green)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-orange)

## 📖 Sobre o Projeto

Este projeto foi desenvolvido para coletar, analisar e visualizar as estimativas populacionais dos municípios brasileiros utilizando dados oficiais do IBGE.

A solução é composta por dois módulos principais:

- Um módulo responsável pela coleta automatizada dos arquivos disponibilizados pelo IBGE.
- Um dashboard interativo responsável pela análise e visualização dos dados.

Dessa forma, o projeto cobre todo o fluxo, desde a obtenção das informações até a geração de relatórios e gráficos para análise.

---

## 🎯 Objetivo

Fornecer uma ferramenta que permita explorar a evolução populacional dos municípios brasileiros de forma simples e visual, utilizando dados públicos oficiais.

Entre os objetivos do projeto estão:

- Centralizar dados populacionais históricos.
- Facilitar consultas por estado e município.
- Identificar tendências de crescimento populacional.
- Gerar relatórios automatizados.
- Transformar dados brutos em informações de fácil interpretação.

---

## 🏗️ Estrutura da Solução

O projeto é dividido em dois componentes principais.

### 📥 downloads_documentos.py

Responsável pela coleta automatizada dos dados.

O script acessa o repositório oficial do IBGE e realiza o download dos arquivos de estimativas populacionais disponíveis para cada ano.

Principais atividades:

- Conexão com o portal do IBGE.
- Busca automática dos arquivos disponíveis.
- Download de arquivos XLS, XLSX, CSV, PDF e ZIP.
- Organização dos documentos em pastas por ano.
- Verificação para evitar downloads duplicados.

Período contemplado:

- 1989 a 2025

Esse módulo funciona como a camada de aquisição de dados do projeto.

---

### 📊 dashboard.py

Responsável pela análise e visualização das informações.

A aplicação foi desenvolvida utilizando Streamlit e permite explorar os dados de forma interativa.

Principais funcionalidades:

- Seleção de estados.
- Escolha do ano de referência.
- Indicadores populacionais.
- Ranking dos municípios mais populosos.
- Classificação por faixas populacionais.
- Comparação entre municípios.
- Gráficos de evolução da população.
- Geração automática de relatórios em PDF.

Além das análises visuais, o sistema produz relatórios contendo tabelas, gráficos e resumos estatísticos.

---

## 🔄 Fluxo do Projeto

```text
Portal do IBGE
       │
       ▼
downloads_documentos.py
       │
       ▼
Arquivos Históricos
       │
       ▼
Base Consolidada
       │
       ▼
dashboard.py
       │
       ▼
Dashboard Interativo + Relatórios PDF
```

---

## 📊 Recursos Disponíveis

### Indicadores

- Município mais populoso.
- Município menos populoso.
- População total.
- Participação percentual dos municípios analisados.

### Rankings

- Top 10 municípios mais populosos.

### Classificação Populacional

- Acima de 1 milhão de habitantes.
- Entre 500 mil e 1 milhão de habitantes.
- Até 500 mil habitantes.

### Evolução Populacional

- Comparação entre municípios.
- Crescimento absoluto.
- Crescimento percentual.
- Visualização temporal por meio de gráficos interativos.

### Relatórios

- Exportação em PDF.
- Tabelas consolidadas.
- Indicadores principais.
- Gráficos de evolução.
- Resumos automáticos dos resultados.

---

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- ReportLab
- Requests
- BeautifulSoup
- OpenPyXL

---

## 📂 Estrutura do Projeto

```text
.
├── dashboard.py
├── downloads_documentos.py
├── populacao.xlsx
├── logo.png
├── IBGE.png
└── README.md
```

---

## ▶️ Como Executar

### Instalar dependências

```bash
pip install streamlit pandas plotly reportlab requests beautifulsoup4 openpyxl kaleido
```

### Executar o dashboard

```bash
streamlit run dashboard.py
```

### Executar a coleta dos dados

```bash
python downloads_documentos.py
```

---

## 📚 Fonte dos Dados

Dados oficiais disponibilizados pelo
:contentReference[oaicite:0]{index=0}.

As estimativas populacionais utilizadas no projeto são públicas e podem ser consultadas diretamente no portal do instituto.

---

## 👨‍💻 Autor

Projeto desenvolvido para fins de análise de dados, automação da coleta de informações públicas e visualização de indicadores demográficos dos municípios brasileiros.