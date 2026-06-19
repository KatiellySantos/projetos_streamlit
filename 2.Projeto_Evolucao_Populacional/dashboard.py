# ============================================================
# APP.PY - DASHBOARD POPULACIONAL E GERAÇÃO DE RELATÓRIO PDF
# ============================================================

# ------------------------------------------------------------
# IMPORTAÇÕES
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio
from datetime import datetime
from zoneinfo import ZoneInfo
import tempfile

# ReportLab - Geração de PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import PageBreak

st.set_page_config(layout="wide")

# ------------------------------------------------------------
# LEITURA E CARREGAMENTO DOS DADOS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)  # CORRIGIDO
file_path = os.path.join(BASE_DIR, "populacao.xlsx")

df = pd.read_excel(file_path)

# ------------------------------------------------------------
# TÍTULO DO DASHBOARD
# ------------------------------------------------------------

st.markdown("""
<style>
.titulo-container{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:4px;}
.titulo-container img{height:48px;}
.titulo-texto{font-size:28px;font-weight:700;color:#002776;margin:0;white-space: nowrap;}
.titulo-linha{width:240px;margin:6px auto 18px auto;height:4px;background:linear-gradient(90deg,#F2B705,#1C4D86);border-radius:6px;}
</style>
<div class="titulo-container">
    <img src="">
    <h1 class="titulo-texto">Estimativa populacional dos municípios ao longo dos anos</h1>
</div>
<div class="titulo-linha"></div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# LEGENDA DO DASHBOARD
# ------------------------------------------------------------

st.markdown(
    """
<div style='width: 100%; text-align: right; padding-right: 10px; color:gray;'>
<a href="https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=downloads" target="_blank">
Fonte dos dados: Estimativas da População - IBGE
</a>
</div>
""",
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# ESTILIZAÇÃO DA SIDEBAR (HTML/CSS)
# ------------------------------------------------------------

# Sidebar fixa na lateral da aplicação
st.markdown(
    """
    <style>
    /* Sidebar fixa */
    section[data-testid="stSidebar"] {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 230px;
        min-width: 230px;
        max-width: 230px;
        overflow-y: auto;
        background-color: inherit;
        z-index: 1000;
    }
    /* Área principal deslocada para não sobrepor a sidebar */
    section.main {
        margin-left: 230px;
    }
    /* Remove botão de recolher */
    button[data-testid="collapsedControl"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# APARÊNCIA DOS COMPONENTES DA SIDEBAR (HTML/CSS)
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    /* Caixa do multiselect */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border: 1px solid #7492C1 !important;
    border-radius: 6px !important;
    width: 140px !important; / largura da caixa */
    }

    /* Menu suspenso (dropdown) */
    section[data-testid="stSidebar"] ul[data-baseweb="menu"] {
    background-color: #7492C1 !important;
    border-radius: 6px !important;
    }

    /* Tags dos itens selecionados */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: transparent !important;
    color: black !important;
    min-width: 60px !important;
    padding: 6px 12px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    border: 1px solid #7492C1 !important;
    
    }
    
    /* Texto das tags */
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: black !important;
    }

    /* Ícone de remoção (X) */
    section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    fill: red !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# FUNÇÃO DE FORMATAÇÃO
# ------------------------------------------------------------

def formatar_brasil(valor):
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "Sem informação"

# ------------------------------------------------------------
# FILTROS DA SIDEBAR
# ------------------------------------------------------------

# Lista de estados disponíveis
estado = sorted(df["ESTADO"].unique())

# Seleção de estados
se_estado = st.sidebar.multiselect(
    "ESTADO",
    estado,
    default=estado
)

# ------------------------------------------------------------
# SELEÇÃO DO ANO DE REFERÊNCIA
# ------------------------------------------------------------

anos = sorted([
    col.replace("POPULACAO_", "")
    for col in df.columns
    if col.startswith("POPULACAO_")
])

se_ano = st.sidebar.selectbox(
    "ANO DE REFERÊNCIA",
    anos,
    index=len(anos) - 1
)

coluna_pop = f"POPULACAO_{se_ano}"

# ------------------------------------------------------------
# FILTRO DOS DADOS
# ------------------------------------------------------------

df_filtrado = df[
    df["ESTADO"].isin(se_estado)
].copy()

if df_filtrado.empty:
    st.warning(
        "Nenhum estado foi selecionado. Escolha pelo menos um estado para visualizar os dados.")
    st.stop()

df_filtrado["POPULACAO"] = df_filtrado[coluna_pop]

# ------------------------------------------------------------
# GRÁFICO INDICADORES POPULACIONAIS
# ------------------------------------------------------------

# Seleciona os 10 municípios mais populosos
municipios_02 = (
    df_filtrado
    .sort_values(by=coluna_pop, ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# Identifica o município mais e menos populoso do ranking
mais_populoso = municipios_02.iloc[0]
menos_populoso = municipios_02.iloc[-1]

# Calcula totais e participação percentual
soma_top10 = municipios_02[coluna_pop].sum()
soma_estado = df_filtrado[coluna_pop].sum()

percentual_top10 = (
    (soma_top10 / soma_estado) * 100
    if soma_estado > 0
    else 0
)

percentual_formatado = f"{percentual_top10:.2f}".replace(".", ",")

# ------------------------------------------------------------
# CARDS DE INDICADORES
# ------------------------------------------------------------

esp1, col1, esp2, col2, esp3, col3, esp4 = st.columns([2, 3, 2, 3, 2, 3, 2])

col1.metric(
    "Município Mais Populoso",
    mais_populoso["MUNICIPIO"],
    f"{formatar_brasil(mais_populoso[coluna_pop])} habitantes"
)

col2.metric(
    "Município Menos Populoso",
    menos_populoso["MUNICIPIO"],
    f"{formatar_brasil(menos_populoso[coluna_pop])} habitantes"
)

col3.metric(
    "População Total",
    formatar_brasil(soma_estado),
    f"{percentual_formatado}% do total"
)

# ------------------------------------------------------------
# DICIONÁRIO DE SIGLAS DOS ESTADOS
# ------------------------------------------------------------

sigla_para_estado = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
}

# ------------------------------------------------------------
# RANKING DOS 10 MUNICÍPIOS MAIS POPULOSOS
# ------------------------------------------------------------

municipios_02["Ranking"] = municipios_02.index + 1

tabela = municipios_02[
    ["Ranking", "MUNICIPIO", coluna_pop]
].rename(
    columns={
        "MUNICIPIO": "Município",
        coluna_pop: f"População {se_ano}"
    }
)

st.subheader("Ranking dos 10 Municípios Mais Populosos")

st.table(
    tabela.style
    .hide(axis="index")
    .format({
        f"População {se_ano}": lambda x: f"{x:,.0f}".replace(",", ".")
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#1F4E79"),
                ("color", "white"),
                ("font-weight", "bold")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("background-color", "#EEF2F7"),
                ("color", "black")
            ]
        }
    ])
)

# ------------------------------------------------------------
# RESUMO DOS RESULTADOS
# ------------------------------------------------------------

st.markdown(f"""

- Em **{se_ano}**, **{mais_populoso['MUNICIPIO']}** foi o município com a maior população estimada entre os estados selecionados (**{', '.join(sigla_para_estado[uf] for uf in se_estado)}**), com aproximadamente **{formatar_brasil(mais_populoso[coluna_pop])} habitantes**.

- **{menos_populoso['MUNICIPIO']}** ocupa a décima colocação com cerca de **{formatar_brasil(menos_populoso[coluna_pop])} habitantes**.
  Juntos, os 10 primeiros colocados somam **{formatar_brasil(soma_top10)} habitantes**, representando **{percentual_formatado}%** da população total.
""")

# ------------------------------------------------------------
# CLASSIFICAÇÃO POR FAIXAS POPULACIONAIS
# ------------------------------------------------------------

st.subheader("Classificação por Faixas Populacionais")

# Separação dos municípios por faixa populacional
faixa_1 = df_filtrado[df_filtrado[coluna_pop] > 1_000_000]
faixa_2 = df_filtrado[(df_filtrado[coluna_pop] > 500_000)
                      & (df_filtrado[coluna_pop] <= 1_000_000)]
faixa_3 = df_filtrado[df_filtrado[coluna_pop] <= 500_000]

# Layout das colunas
coluna_1, coluna_2, coluna_3 = st.columns([10, 10, 10])

# ------------------------------------------------------------
# FAIXA 1 - ACIMA DE 1 MILHÃO DE HABITANTES
# ------------------------------------------------------------

with coluna_1:
    quantidade = len(faixa_1)
    texto = "município" if quantidade == 1 else "municípios"

    st.markdown(f"🔴 **Acima de 1 milhão:** {quantidade:,.0f}".replace(",", ".")
                + f" {texto}")

    tabela_1 = pd.DataFrame()
    if not faixa_1.empty:
        tabela_1 = faixa_1[["MUNICIPIO", coluna_pop]].rename(columns={
            "MUNICIPIO": "Município",
            coluna_pop: f"População {se_ano}"
        }).sort_values(by=f"População {se_ano}", ascending=False)
        tabela_1[f"População {se_ano}"] = (
            tabela_1[f"População {se_ano}"].apply(
                lambda x: f"{x:,.0f}".replace(",", "."))
        )

    else:
        st.info("Não há municípios nesta faixa populacional para o estado selecionado.")
    
    # Estilo da tabela
    st.markdown("""
    <style>
    .tabela-scroll {
        max-height: 300px;
        overflow-y: auto;                
             border: 1px solid #ddd;
    }

    .tabela-scroll table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .tabela-scroll th {
        position: sticky;
        top: 0;
        background-color: #1F4E79;
        color: white;
        padding: 8px;
        text-align: left;
    }

    .tabela-scroll td {
        background-color: #EEF2F7;
        color: black;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

    html_tabela = tabela_1.to_html(index=False)

    st.markdown(
        f'<div class="tabela-scroll">{html_tabela}</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# FAIXA 2 - ENTRE 500 MIL E 1 MILHÃO DE HABITANTES
# ------------------------------------------------------------

with coluna_2:
    quantidade = len(faixa_2)
    texto = "município" if quantidade == 1 else "municípios"

    st.markdown(f"🟠 **Entre 500 mil e 1 milhão:** {quantidade:,.0f}".replace(",", ".")
                + f" {texto}")

    tabela_2 = pd.DataFrame()
    if not faixa_2.empty:
        tabela_2 = faixa_2[["MUNICIPIO", coluna_pop]].rename(columns={
            "MUNICIPIO": "Município",
            coluna_pop: f"População {se_ano}"
        }).sort_values(
            by=f"População {se_ano}",
            ascending=False
        )

        tabela_2[f"População {se_ano}"] = (
            tabela_2[f"População {se_ano}"]
            .apply(lambda x: f"{x:,.0f}".replace(",", "."))
        )
    else:
        st.info("Não há municípios nesta faixa populacional para o estado selecionado.")

    # Estilo da tabela
    st.markdown("""
    <style>
    .tabela-scroll {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
    }

    .tabela-scroll table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .tabela-scroll th {
        position: sticky;
        top: 0;
        background-color: #1F4E79;
        color: white;
        padding: 8px;
        text-align: left;
    }

    .tabela-scroll td {
        background-color: #EEF2F7;
        color: black;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    </style>
        """, unsafe_allow_html=True)

    html_tabela = tabela_2.to_html(index=False)

    st.markdown(
        f'<div class="tabela-scroll">{html_tabela}</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# FAIXA 3 - ABAIXO DE 500 MIL HABITANTES
# ------------------------------------------------------------

with coluna_3:
    quantidade = len(faixa_3)
    texto = "município" if quantidade == 1 else "municípios"

    st.markdown(f"🟢 **Abaixo de 500 mil:** {quantidade:,.0f}".replace(",", ".")
                + f" {texto}")

    tabela_3 = pd.DataFrame()
    if not faixa_3.empty:
        tabela_3 = faixa_3[["MUNICIPIO", coluna_pop]].rename(columns={
            "MUNICIPIO": "Município",
            coluna_pop: f"População {se_ano}"
        }).sort_values(by=f"População {se_ano}", ascending=False
                       )

        tabela_3[f"População {se_ano}"] = (
            tabela_3[f"População {se_ano}"]
            .apply(lambda x: f"{x:,.0f}".replace(",", "."))
        )
    else:
        st.info("Não há municípios nesta faixa populacional para o estado selecionado.")

    # Estilo da tabela
    st.markdown("""
    <style>
    .tabela-scroll {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
    }

    .tabela-scroll table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .tabela-scroll th {
        position: sticky;
        top: 0;
        background-color: #1F4E79;
        color: white;
        padding: 8px;
        text-align: left;
    }

    .tabela-scroll td {
        background-color: #EEF2F7;
        color: black;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    </style>
        """, unsafe_allow_html=True)

    html_tabela = tabela_3.to_html(index=False)

    st.markdown(
        f'<div class="tabela-scroll">{html_tabela}</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# ESTILIZAÇÃO DOS FILTROS DE EVOLUÇÃO POPULACIONAL
# ------------------------------------------------------------

st.markdown("""
<style>
            
/* Caixa principal dos multiselects */            
div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border: 1px solid #7492C1 !important;
    border-radius: 6px !important;
}

/* Menu suspenso (dropdown) */
ul[data-baseweb="menu"] {
    background-color: #7492C1 !important;
    border-radius: 6px !important;
}

/* Tags dos itens selecionados */
[data-baseweb="tag"] {
    background-color: transparent !important;
    color: black !important;
    min-width: 80px !important;
    padding: 6px 12px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    border: 1px solid #7492C1 !important;
}

/* Texto das tags */
[data-baseweb="tag"] span {
    color: black !important;
}

/* Ícone de remoção (X) */
[data-baseweb="tag"] svg {
    fill: red !important;
}           

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FILTROS DE EVOLUÇÃO POPULACIONAL
# ------------------------------------------------------------

municipios_estado = sorted(df_filtrado["MUNICIPIO"].unique())

#Espaçamento entre seções
st.write("")
st.write("")

municipios_selecionados = st.multiselect(
    "Selecione um ou mais municípios para visualizar a evolução populacional:",
    municipios_estado,
    default=[]
)

anos_comparacao = st.multiselect(
    "Selecione os anos para comparação:",
    anos,
    default=[anos[0], anos[-1]]
)

# ------------------------------------------------------------
# EVOLUÇÃO POPULACIONAL DOS MUNICÍPIOS
# ------------------------------------------------------------

if municipios_selecionados and anos_comparacao:

    # Título da seção
    titulo_evolucao = ", ".join(municipios_selecionados)

    st.subheader(
        f"Evolução da População ao longo dos anos em: {titulo_evolucao}"
    )
    
    # Colunas populacionais correspondentes aos anos selecionados
    anos_cols = sorted(
        [f"POPULACAO_{ano}" for ano in anos_comparacao],
        key=lambda x: int(x.replace("POPULACAO_", ""))
    )
    
    # Filtra os municípios selecionados
    df_long = df_filtrado[
        df_filtrado["MUNICIPIO"].isin(municipios_selecionados)
    ]
    
    # Converte os dados para formato longo
    df_long = df_long.melt(
        id_vars=["MUNICIPIO"],
        value_vars=anos_cols,
        var_name="Ano",
        value_name="População"
    )

    # Ajusta o formato do ano
    df_long["Ano"] = (
        df_long["Ano"]
        .str.replace("POPULACAO_", "")
        .astype(int)
    )

    # --------------------------------------------------------
    # FORMATAÇÃO DOS DADOS PARA O HOVER
    # --------------------------------------------------------

    df_long["Populacao_hover"] = (
        df_long["População"]
        .fillna(0)
        .astype(int)
        .apply(lambda x: f"{x:,}".replace(",", "."))
    )

    fig_line = px.line(
        df_long,
        x="Ano",
        y="População",
        color="MUNICIPIO",
        markers=True,
        labels={
            "Ano": "Ano",
            "População": "População",
            "MUNICIPIO": "Município"
        },
    )

    # --------------------------------------------------------
    # GRÁFICO DE EVOLUÇÃO POPULACIONAL
    # --------------------------------------------------------

    fig_line.update_traces(
        customdata=df_long[["Populacao_hover"]],
        hovertemplate="<b>%{fullData.name}</b><br>" +
        "Ano: %{x}<br>" +
        "População: %{customdata[0]} habitantes<extra></extra>"
    )

    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            title=None,
            tickfont=dict(color="#1A1A1A")
        ),
        xaxis=dict(
            title=None,
            tickfont=dict(color="#1A1A1A")
        ),
        legend_title_text="Município"
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True,
        key="grafico_populacao"
    )

    # --------------------------------------------------------
    # ANÁLISE DE CRESCIMENTO POR MUNICÍPIO
    # --------------------------------------------------------

    for municipio in municipios_selecionados:

        df_munic = df_filtrado[
            df_filtrado["MUNICIPIO"] == municipio
        ]

        try:
            valor_inicio = int(df_munic[anos_cols[0]].values[0])
            valor_fim = int(df_munic[anos_cols[-1]].values[0])
        except (ValueError, TypeError):
            st.warning(
                f"Dados indisponíveis para {municipio} em um dos anos selecionados."
            )
            continue

        ano_inicio = anos_cols[0].replace("POPULACAO_", "")
        ano_fim = anos_cols[-1].replace("POPULACAO_", "")

        crescimento_abs = valor_fim - valor_inicio

        crescimento_pct = (
            ((valor_fim - valor_inicio) / valor_inicio) * 100
            if valor_inicio
            else 0
        )

        crescimento_pct_formatado = (
            f"{crescimento_pct:.2f}"
            .replace(".", ",")
        )

        st.markdown(f"""
- O município **{municipio}** possuía cerca de **{formatar_brasil(valor_inicio)} habitantes** em {ano_inicio}.
  Em {ano_fim}, passou para **{formatar_brasil(valor_fim)} habitantes**.
  Isso representa uma variação absoluta de **{formatar_brasil(crescimento_abs)} habitantes**.
  A variação percentual no período foi de **{crescimento_pct_formatado}%**.
""")
        
# Mensagem quando não há seleção
else:
    st.info(
        "Selecione pelo menos um município e um ano para visualizar a evolução populacional."
    )


# ------------------------------------------------------------
# RELATÓRIO PDF
# ------------------------------------------------------------

# Configuração inicial do relatório PDF
styles = getSampleStyleSheet()
story = []

# Logo do IBGE
ibge_path = os.path.join(BASE_DIR, "IBGE.png")

if os.path.exists(ibge_path):
    logo = Image(ibge_path, width=60, height=60)
    story.append(logo)
    story.append(Spacer(1, 6))

# Título do relatório
story.append(
    Paragraph(
        "Estimativa populacional dos municípios ao longo dos anos",
        styles["Title"]
    )
)

# Data e hora de geração
agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
data_formatada = agora.strftime("%d/%m/%Y %H:%M")

styles.add(
    ParagraphStyle(
        name="DataDireita",
        parent=styles["Normal"],
        fontSize=8,
        alignment=TA_RIGHT
    )
)

story.append(
    Paragraph(
        f"Gerado em: {data_formatada}",
        styles["DataDireita"]
    )
)

story.append(Spacer(1, 16))

# Texto de introdução
styles.add(
    ParagraphStyle(
        name="TextoIntroducao",
        parent=styles["Normal"],
        fontSize=11,  # aumente aqui
        leading=14
    )
)

# Indicadores principais (KPIs)
story.append(
    Paragraph(
        """
        Este relatório apresenta uma análise das estimativas populacionais dos municípios
        selecionados ao longo dos anos, com base nos dados disponíveis. São apresentados
        indicadores gerais, ranking dos municípios mais populosos, distribuição por faixas
        populacionais e a evolução da população nos períodos escolhidos. O objetivo é
        fornecer uma visão consolidada do comportamento demográfico, permitindo identificar
        padrões de crescimento, redução e concentração populacional entre os municípios
        analisados.
        """,
        styles["TextoIntroducao"]
    )
)

story.append(Spacer(1, 18))

kpis = [
    f"Município Mais Populoso\n{mais_populoso['MUNICIPIO']}\n{formatar_brasil(mais_populoso[coluna_pop])} habitantes",
    f"Município Menos Populoso\n{menos_populoso['MUNICIPIO']}\n{formatar_brasil(menos_populoso[coluna_pop])} habitantes",
    f"População Total\n{formatar_brasil(soma_estado)}\n{percentual_formatado}% do total"
]

tabela_kpi = [kpis]

t = Table(tabela_kpi, colWidths=[2.5*inch]*3, hAlign="CENTER")
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white)
]))

story.append(t)
story.append(Spacer(1, 12))

# ------------------------------------------------------------
# RANKING DOS 10 MUNICÍPIOS MAIS POPULOSOS
# ------------------------------------------------------------

story.append(
    Paragraph("Ranking dos 10 Municípios Mais Populosos", styles["Heading2"]))
story.append(Spacer(1, 10))

dados_tabela = [[" Ranking", "Município", f"População {se_ano}"]]

for _, row in tabela.iterrows():
    dados_tabela.append([
        row["Ranking"],
        row["Município"],
        formatar_brasil(row[f"População {se_ano}"])
    ])

tabela_pdf = Table(
    dados_tabela,
    colWidths=[1*inch, 3*inch, 2*inch],
    hAlign="LEFT"
)

tabela_pdf.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]))

story.append(tabela_pdf)
story.append(Spacer(1, 12))

# ------------------------------------------------------------
# RESUMO DOS RESULTADOS
# ------------------------------------------------------------

texto_resumo = f"""
• Em <b>{se_ano}</b>, <b>{mais_populoso['MUNICIPIO']}</b> foi o município com a maior população estimada entre os estados selecionados ({', '.join(sigla_para_estado[uf] for uf in se_estado)}), com aproximadamente <b>{formatar_brasil(mais_populoso[coluna_pop])} habitantes</b>.<br/><br/>
• <b>{menos_populoso['MUNICIPIO']}</b> ocupa a décima colocação com cerca de <b>{formatar_brasil(menos_populoso[coluna_pop])} habitantes</b>; juntos, os 10 municípios mais populosos somam <b>{formatar_brasil(soma_top10)} habitantes</b>, representando <b>{percentual_formatado}%</b> da população total.
"""

story.append(Paragraph(texto_resumo, styles["BodyText"]))
story.append(Spacer(1, 12))
story.append(PageBreak())

# -------------------------------------------------------------
# CLASSIFICAÇÃO POR FAIXAS POPULACIONAIS
# -------------------------------------------------------------

story.append(
    Paragraph(
        "Classificação por Faixas Populacionais",
        styles["Heading2"]
    )
)

story.append(Spacer(1, 10))

# Estilo dos subtítulo das faixas
styles.add(
    ParagraphStyle(
        name="SubtituloSemNegrito",
        parent=styles["Normal"],
        fontSize=12,
        leading=16
    )
)

# ------------------------------------------------------------
# FAIXA 1 - ACIMA DE 1 MILHÃO DE HABITANTES
# ------------------------------------------------------------

quantidade = len(faixa_1)
texto = "município" if quantidade == 1 else "municípios"

story.append(
    Paragraph(
        f"Acima de 1 milhão: {quantidade:,.0f} {texto}".replace(",", "."),
        styles["SubtituloSemNegrito"]
    )
)

story.append(Spacer(1, 4))

if not tabela_1.empty:

    tabela_1_pdf = tabela_1.head(10)
    dados = [list(tabela_1_pdf.columns)] + tabela_1_pdf.values.tolist()

    tabela_pdf = Table(
        dados,
        colWidths=[160, 160],
        hAlign="LEFT"
    )

    tabela_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    story.append(tabela_pdf)

else:
    story.append(
        Paragraph(
            "Não há municípios nesta faixa populacional.",
            styles["Normal"]
        )
    )

story.append(Spacer(1, 15))

# ------------------------------------------------------------
# FAIXA 2 - ENTRE 500 MIL E 1 MILHÃO DE HABITANTES
# ------------------------------------------------------------

quantidade = len(faixa_2)
texto = "município" if quantidade == 1 else "municípios"

story.append(
    Paragraph(
        f"Entre 500 mil e 1 milhão: {quantidade:,.0f} {texto}".replace(
            ",", "."),
        styles["SubtituloSemNegrito"]
    )
)

story.append(Spacer(1, 4))

if not tabela_2.empty:

    tabela_2_pdf = tabela_2.head(10)
    dados = [list(tabela_2_pdf.columns)] + tabela_2_pdf.values.tolist()

    tabela_pdf = Table(
        dados,
        colWidths=[160, 160],
        hAlign="LEFT"
    )

    tabela_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    story.append(tabela_pdf)

else:
    story.append(
        Paragraph(
            "Não há municípios nesta faixa populacional.",
            styles["Normal"]
        )
    )

story.append(Spacer(1, 15))

# ------------------------------------------------------------
# FAIXA 3 - ABAIXO DE 500 MIL HABITANTES
# ------------------------------------------------------------

quantidade = len(faixa_3)
texto = "município" if quantidade == 1 else "municípios"

story.append(
    Paragraph(
        f"Abaixo de 500 mil: {quantidade:,.0f} {texto}".replace(",", "."),
        styles["SubtituloSemNegrito"]
    )
)

story.append(Spacer(1, 4))

if not tabela_3.empty:

    tabela_3_pdf = tabela_3.head(10)
    dados = [list(tabela_3_pdf.columns)] + tabela_3_pdf.values.tolist()

    tabela_pdf = Table(
        dados,
        colWidths=[160, 160],
        hAlign="LEFT"
    )

    tabela_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    story.append(tabela_pdf)

else:
    story.append(
        Paragraph(
            "Não há municípios nesta faixa populacional.",
            styles["Normal"]
        )
    )

story.append(Spacer(1, 15))
story.append(PageBreak())

# ============================================================
# EVOLUÇÃO POPULACIONAL DOS MUNICÍPIOS (PDF)
# ============================================================

if municipios_selecionados and anos_comparacao:

    # --------------------------------------------------------
    # PREPARAÇÃO DOS DADOS
    # --------------------------------------------------------

    titulo_evolucao = ", ".join(municipios_selecionados)

    anos_cols = sorted(
        [f"POPULACAO_{ano}" for ano in anos_comparacao],
        key=lambda x: int(x.replace("POPULACAO_", ""))
    )

    df_long_pdf = df_filtrado[
        df_filtrado["MUNICIPIO"].isin(municipios_selecionados)
    ]

    df_long_pdf = df_long_pdf.melt(
        id_vars=["MUNICIPIO"],
        value_vars=anos_cols,
        var_name="Ano",
        value_name="População"
    )

    df_long_pdf["Ano"] = (
        df_long_pdf["Ano"]
        .str.replace("POPULACAO_", "")
        .astype(int)
    )

    # --------------------------------------------------------
    # GRÁFICO DE EVOLUÇÃO POPULACIONAL
    # --------------------------------------------------------

    fig_line_pdf = px.line(
        df_long_pdf,
        x="Ano",
        y="População",
        color="MUNICIPIO",
        markers=True,
        labels={
            "Ano": "Ano",
            "População": "População",
            "MUNICIPIO": "Município"
        }
    )

    fig_line_pdf.update_layout(
        width=900,
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title_text="Município"
    )

    # --------------------------------------------------------
    # TÍTULO DA SEÇÃO NO PDF
    # --------------------------------------------------------

    story.append(
        Paragraph(
            f"Evolução da População - {titulo_evolucao}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    # --------------------------------------------------------
    # EXPORTAÇÃO DO GRÁFICO PARA IMAGEM
    # --------------------------------------------------------

    with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    ) as tmpfile:

        fig_line_pdf.write_image(tmpfile.name)

        story.append(
            Image(
                tmpfile.name,
                width=450,
                height=250
            )
        )

    story.append(Spacer(1, 10))

    # --------------------------------------------------------
    # ANÁLISE DE CRESCIMENTO DOS MUNICÍPIOS
    # --------------------------------------------------------

    for municipio in municipios_selecionados:

        df_munic = df_filtrado[
            df_filtrado["MUNICIPIO"] == municipio
        ]

        try:
            valor_inicio = int(df_munic[anos_cols[0]].values[0])
            valor_fim = int(df_munic[anos_cols[-1]].values[0])
        except (ValueError, TypeError, IndexError):
            continue

        ano_inicio = anos_cols[0].replace("POPULACAO_", "")
        ano_fim = anos_cols[-1].replace("POPULACAO_", "")

        crescimento_abs = valor_fim - valor_inicio

        crescimento_pct = (
            ((valor_fim - valor_inicio) / valor_inicio) * 100
            if valor_inicio
            else 0
        )

        crescimento_pct_formatado = (
            f"{crescimento_pct:.2f}"
            .replace(".", ",")
        )

        texto = f"""
            • O município <b>{municipio}</b> possuía cerca de
            <b>{formatar_brasil(valor_inicio)} habitantes</b> em {ano_inicio}.
            Em {ano_fim}, passou para
            <b>{formatar_brasil(valor_fim)} habitantes</b>.
            Isso representa uma variação absoluta de
            <b>{formatar_brasil(crescimento_abs)} habitantes</b>.
            A variação percentual no período foi de
            <b>{crescimento_pct_formatado}%</b>.
        """

        story.append(
            Paragraph(
                texto,
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 6))

# ============================================================
# LOGO E ASSINATURA FINAL
# ============================================================

logo_path = os.path.join(BASE_DIR, "logo.png")
if os.path.exists(logo_path):
    logo_final = Image(logo_path, width=60, height=60)
    assinatura = Table([['', logo_final]], colWidths=[400, 60])
    assinatura.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT')
    ]))
story.append(Spacer(1, 20))
story.append(assinatura)
story.append(Spacer(1, 20))

# ============================================================
# GERAÇÃO DO ARQUIVO PDF
# ============================================================

tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

doc = SimpleDocTemplate(
    tmp_pdf.name,
    pagesize=A4,
    topMargin=25,
    bottomMargin=25
)

doc.build(story)

with open(tmp_pdf.name, "rb") as f:
    pdf_bytes = f.read()

# ------------------------------------------------------------
# ESTILIZAÇÃO DO BOTÃO DE DOWNLOAD
# ------------------------------------------------------------

st.markdown("""
<style>
.stDownloadButton > button {
    background-color: transparent !important;
    border: 1px solid #7492C1 !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    padding: 0.2rem 0.6rem !important;
    min-height: 32px !important;
    font-size: 13px !important;
    width: 140px !important;
}

.stDownloadButton > button:hover {
    background-color: transparent !important;
    border-color: #666 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# BOTÃO DE DOWNLOAD DO RELATÓRIO
# ------------------------------------------------------------

st.sidebar.download_button(
    label="📄 Gerar Relatório em PDF",
    data=pdf_bytes,
    file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    mime="application/pdf",
    key="download_pdf"
)

# ------------------------------------------------------------
# LOGO DA BARRA LATERAL
# ------------------------------------------------------------

logo_path = os.path.join(BASE_DIR, ".png")
col1, col2, col3 = st.sidebar.columns([1, 4, 3])

with col2:
    st.image(logo_path, width=260)

# ------------------------------------------------------------
# Estilo do Dashboard
# ------------------------------------------------------------

st.markdown("""
<style>

/* Fundo geral da aplicação */
html, body {
    background-color: #EEF2F7 !important;
    height: 100%;
    margin: 0;
    padding: 0;
}

/* Mantém os containers transparentes para exibir o fundo */
.stApp, .block-container, .st-emotion-cache-12fmjuu, section.main {
    background: transparent !important;
}

/* Sidebar com efeito de transparência e sombra */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0) !important;
    backdrop-filter: blur(6px);  
    box-shadow: 8px 0 18px rgba(0,0,0,0.25);  /* SOMBRA lateral da esquerda para a direita */
    z-index: 10;
}

/* Cabeçalho do Streamlit */
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0) !important;
}

/* Rodapé */
footer, .stFooter {
    background: rgba(0, 0, 0, 0) !important;
}

/* Container principal do dashboard com leve sombra */
.block-container {
    box-shadow: 0 0 22px rgba(0,0,0,0.18);
    border-radius: 12px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)
