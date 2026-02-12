# ============================
# app.py — Painel + Relatório PDF (final)
# ============================

# ---------- IMPORTS ----------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
from datetime import datetime
import tempfile
import os

# reportlab para montar PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

# ---------- CONFIG PAGE ----------
st.set_page_config(
    page_title="Painel Econômico e Turístico",
    page_icon=".png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- LEITURA DO ARQUIVO ----------
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "planilha.xlsx")
df = pd.read_excel(file_path)

# ---------- TÍTULO (HTML/CSS) ----------
st.markdown("""
<style>
.titulo-container{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:4px;}
.titulo-container img{height:48px;}
.titulo-texto{font-size:28px;font-weight:700;color:#002776;margin:0;}
.titulo-linha{width:240px;margin:6px auto 18px auto;height:4px;background:linear-gradient(90deg,#F2B705,#1C4D86);border-radius:6px;}
</style>
<div class="titulo-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/3/3e/IBGE-Brazil.svg">
    <h1 class="titulo-texto">Painel de Desenvolvimento Econômico e Turístico</h1>
</div>
<div class="titulo-linha"></div>
""", unsafe_allow_html=True)

# ---------- LEGENDA do DASHBOARD ----------
st.markdown(
    """
    <div style='width: 100%; text-align: right; padding-right: 10px;'>
        <span style='font-size: 0.8em; color: black; font-weight: bold;'>
        Dados extraídos do Mapa do Turismo Brasileiro (ano-base 2018)
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- BARRA LATERAL FIXA (HTML/CSS) ----------
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
    /* Área principal deslocada para não sobrepor */
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

# ---------- APARÊNCIA DA BARRA LATERAL (HTML/CSS) ----------
st.markdown(
    """
    <style>
    /* Caixa do multiselect */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: transparent !important;
        border: 1px solid #7492C1 !important;
        border-radius: 6px !important;
        width: 140px !important;   /* largura da caixa */
        max-width: 140px !important;

    }
    /* Dropdown */
    section[data-testid="stSidebar"] ul[data-baseweb="menu"] {
        background-color: #7492C1 !important;
        border-radius: 6px !important;
    }
    /* Texto dentro da caixa */
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: white !important;
    }
    /* Tags dos itens selecionados */
    section[data-testid="stSidebar"] div[data-baseweb="tag-list"] div span {
        background-color: #7492C1 !important;  /* cor de fundo da tag */
        color: white !important;               /* cor do texto */
        border-radius: 6px !important;
        padding: 2px 6px !important;
        font-weight: bold;
    }
    /* Botão de remover da tag (x) */
    section[data-testid="stSidebar"] div[data-baseweb="tag-list"] div span svg {
        fill: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- BARRA LATERAL ----------

estado = sorted(df["Estado"].unique())
se_estado = st.sidebar.multiselect("Estado", estado, default=estado
                                   )

municipio = sorted(df[df["Estado"].isin(se_estado)]["Município"].unique())
se_municipio = st.sidebar.multiselect("Município", municipio, default=municipio
                                      )
turismo = sorted(df[(df["Estado"].isin(se_estado)) & (
    df["Município"].isin(se_municipio))]["Região Turística"].unique())
se_turismo = st.sidebar.multiselect("Região Turística", turismo, default=turismo
                                    )

df_filtrado = df[
    (df["Estado"].isin(se_estado)) &
    (df["Município"].isin(se_municipio)) &
    (df["Região Turística"].isin(se_turismo))
].copy()

# ---------- FUNÇÃO KPI ----------

def calcula_kpis(df):
    total_empregos = int(df["Empregos"].sum())
    qtd_estabelecimentos = int(df["Estabelecimentos"].sum())
    visitas_nac = int(df["Visitas Nacionais"].sum())
    visitas_int = int(df["Visitas Internacionais"].sum())
    arrecadacao = float(df["Arrecadação"].sum())
    return total_empregos, qtd_estabelecimentos, visitas_nac, visitas_int, arrecadacao


total_empregos, qtd_estabelecimentos, visitas_nac, visitas_int, arrecadacao = calcula_kpis(
    df_filtrado)

# ---------- KPIs NA TELA ----------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div style="background-color:#1C4D86;padding:16px;border-radius:10px;text-align:center;color:white;">
        <div style="font-size:14px;opacity:0.9">Total de Empregos</div>
        <div style="font-size:20px;font-weight:700">{f"{total_empregos:,}".replace(',', '.')}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background-color:#1C4D86;padding:16px;border-radius:10px;text-align:center;color:white;">
        <div style="font-size:14px;opacity:0.9">Total Estabelecimentos</div>
        <div style="font-size:20px;font-weight:700">{f"{qtd_estabelecimentos:,}".replace(',', '.')}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="background-color:#1C4D86;padding:16px;border-radius:10px;text-align:center;color:white;">
        <div style="font-size:14px;opacity:0.9">Visitas Nacionais</div>
        <div style="font-size:20px;font-weight:700">{f"{visitas_nac:,}".replace(',', '.')}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style="background-color:#1C4D86;padding:16px;border-radius:10px;text-align:center;color:white;">
        <div style="font-size:14px;opacity:0.9">Visitas Internacionais</div>
        <div style="font-size:20px;font-weight:700">{f"{visitas_int:,}".replace(',', '.')}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div style="background-color:#1C4D86;padding:16px;border-radius:10px;text-align:center;color:white;">
        <div style="font-size:14px;opacity:0.9">Arrecadação</div>
        <div style="font-size:20px;font-weight:700">{f"R$ {arrecadacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- ABAS ----------
tab1, tab2, tab3 = st.tabs(
    ["📊 Indicadores do Turismo", "📈 Indicadores de Arrecadação", "📄 Relatório (PDF)"])

# ------------------------------------------------------------
# TAB 1 — TURISMO
# ------------------------------------------------------------
with tab1:
    st.subheader("Empregos e Estabelecimentos Turísticos")
    col_left, _, col_right = st.columns([2, 0.1, 2])

    # Gráfico --> Quantidade de empregos por Estado
    with col_left:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Quantidade de empregos por Estado"
            "</h5>",
            unsafe_allow_html=True
        )
        empre_uf = df_filtrado.groupby(
            "Estado")[["Empregos"]].sum().reset_index()
        empre_uf["hover"] = empre_uf["Empregos"].apply(
            lambda x: f"{x:,.0f}".replace(",", ".") if pd.notna(x) else "0"
        )
        fig_barras = px.bar(empre_uf, x="Estado", y="Empregos", height=420
                            )
        fig_barras.update_traces(marker=dict(color="#1C4D86"),
                                 customdata=empre_uf[["hover"]],
                                 hovertemplate="<b>%{x}</b><br>%{customdata[0]}<extra></extra>"
                                 )
        fig_barras.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # fundo da área do gráfico
            paper_bgcolor="rgba(0,0,0,0)",  # fundo externo
            yaxis=dict(title=None, tickfont=dict(color="#1A1A1A")),
            xaxis=dict(title=None, tickfont=dict(color="#1A1A1A"))
        )
        st.plotly_chart(fig_barras, use_container_width=True, key="grafico_empregos")

    # Gráfico --> Quantidade de estabelecimentos turísticos por Estado
    with col_right:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Quantidade de estabelecimentos turísticos por Estado"
            "</h5>",
            unsafe_allow_html=True
        )
        estabe_uf = df_filtrado.groupby("Estado", as_index=False)[
            ["Estabelecimentos"]].sum()
        estabe_uf["hover"] = estabe_uf["Estabelecimentos"].apply(
            lambda x: f"{x:,.0f}".replace(",", ".") if pd.notna(x) else "0"
        )
        fig_barras_02 = px.bar(estabe_uf, x="Estado", y="Estabelecimentos", height=420
                               )
        fig_barras_02.update_traces(marker=dict(color="#1C4D86"),
                                    customdata=estabe_uf[["hover"]],
                                    hovertemplate="<b>%{x}</b><br>%{customdata[0]}<extra></extra>"
                                    )
        fig_barras_02.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title=None, tickfont=dict(color="#1A1A1A")),
            xaxis=dict(title=None, tickfont=dict(color="#1A1A1A"))
        )
        st.plotly_chart(fig_barras_02, use_container_width=True, key="grafico_estabelecimentos" )

    st.markdown("---")

    st.subheader("Panorama de Visitas")
    col_left, _, col_right = st.columns([2, 0.1, 2])

    # Gráfico --> Comparação entre visitas nacionais e internacionais
    with col_left:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Comparação entre visitas nacionais e internacionais"
            "</h5>",
            unsafe_allow_html=True
        )
        visitas = (df_filtrado.groupby("Estado", as_index=False)[["Visitas Nacionais", "Visitas Internacionais"]].sum()
                   .sort_values(by="Visitas Nacionais", ascending=False)
                   )
        ordem_estados = visitas["Estado"].tolist()

        df_long = visitas.melt(id_vars="Estado", var_name="Tipo", value_name="Quantidade"
                               )
        df_long["Tipo"] = df_long["Tipo"].str.strip()

        df_long["Tipo"] = pd.Categorical(df_long["Tipo"], categories=["Visitas Internacionais", "Visitas Nacionais"],
                                         ordered=True
                                         )
        df_long["hover"] = df_long["Quantidade"].apply(
            lambda x: f"{x:,.0f}".replace(",", ".") if pd.notna(x) else "0"
        )
        fig_barrasVisitas = px.bar(df_long, x="Quantidade", y="Estado", orientation='h',
                                   color="Tipo", barmode="group", height=540,
                                   category_orders={"Tipo": ["Visitas Internacionais", "Visitas Nacionais"],
                                                    "Estado": ordem_estados},
                                   color_discrete_map={
                                       "Visitas Internacionais": "#F5A623", "Visitas Nacionais": "#1C4D86"}
                                   )
        fig_barrasVisitas.update_traces(
            selector=dict(name="Visitas Nacionais"),
            customdata=df_long[df_long["Tipo"] ==
                               "Visitas Nacionais"][["hover"]],
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<extra></extra>"
        )
        fig_barrasVisitas.update_traces(
            selector=dict(name="Visitas Internacionais"),
            customdata=df_long[df_long["Tipo"] ==
                               "Visitas Internacionais"][["hover"]],
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<extra></extra>"
        )
        fig_barrasVisitas.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend=dict(traceorder="reversed"),
            yaxis=dict(title=None, tickfont=dict(color="#1A1A1A")),
            xaxis=dict(title=None, tickfont=dict(
                color="#1A1A1A"), showgrid=True)
        )
        st.plotly_chart(fig_barrasVisitas, use_container_width=True, key="grafico_visitas")

    # Gráfico --> Visitas por Município
    with col_right:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Visitas por Município"
            "</h5>",
            unsafe_allow_html=True
        )
        # Caminho absoluto para o arquivo geojson
        geojson_path = os.path.join(BASE_DIR, "mapa.json")
        
        # Abrir o arquivo com tratamento de erro
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                geojson_mapa = json.load(f)
        except FileNotFoundError:
            st.error(f"Arquivo 'mapa.json' não encontrado em: {geojson_path}")
            st.stop()  # Para a execução do app se o arquivo não existir
        
        df_filtrado["codigo_ibge"] = df_filtrado["codigo_ibge"].astype(str)
        df_filtrado["Visitas_hover"] = df_filtrado["Visitas"].apply(
            lambda x: f" {x:,.0f}".replace(",", ".") if pd.notna(x) else "0"
        )
        fig_mapa_02 = px.choropleth_mapbox(
            df_filtrado,
            geojson=geojson_mapa,
            locations="codigo_ibge",
            featureidkey="properties.id",
            hover_name="Município",
            custom_data=["Visitas_hover"],
            hover_data={"codigo_ibge": False, },  # mostra valor
            mapbox_style="carto-positron",
            center={"lat": -10, "lon": -52},
            zoom=3.3,
            opacity=0.7,
            height=520
        )
        fig_mapa_02.update_traces(hovertemplate="<b>%{hovertext}</b><br>" +
                                  "<br>%{customdata[0]}<extra></extra>")
        fig_mapa_02.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        st.plotly_chart(fig_mapa_02, use_container_width=True, key="grafico_mapa_visitas")

# ------------------------------------------------------------
# TAB 2 — ARRECADAÇÃO
# ------------------------------------------------------------
with tab2:
    st.subheader("Arrecadação Turística")
    col_left, _, col_right = st.columns([2, 0.1, 2])

    # Gráfico --> Evolução da arrecadação turística
    with col_left:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Evolução da arrecadação turística"
            "</h5>",
            unsafe_allow_html=True
        )
        arrecadacaoEstado = (df_filtrado.groupby("Estado", as_index=False)["Arrecadação"].sum()
                             )
        arrecadacaoEstado["Arrecadacao_hover"] = arrecadacaoEstado["Arrecadação"].apply(
            lambda x: f"R$ {x:,.0f}".replace(
                ",", "X").replace(".", ",").replace("X", ".")
        )
        fig_linhas = px.line(arrecadacaoEstado, x="Estado", y="Arrecadação", height=520,
                             color_discrete_sequence=["#F5A623"]
                             )
        fig_linhas.update_traces(
            customdata=arrecadacaoEstado[["Arrecadacao_hover"]],
            hovertemplate="<b>%{x}</b><br>%{customdata[0]}<extra></extra>"
        )
        fig_linhas.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title=None, tickfont=dict(color="#1A1A1A")),
            xaxis=dict(title=None, tickfont=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_linhas, use_container_width=True, key="grafico_arrecadacao")

    # Gráfico --> Arrecadação por Município
    with col_right:
        st.markdown(
            "<h5 style='color:white; text-align:left; margin-bottom:14px;'>"
            "Arrecadação por Município"
            "</h5>",
            unsafe_allow_html=True
        )
        # Caminho absoluto para o arquivo geojson
        geojson_path = os.path.join(BASE_DIR, "mapa.json")
        
        # Abrir o arquivo com tratamento de erro
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                geojson_mapa = json.load(f)
        except FileNotFoundError:
            st.error(f"Arquivo 'mapa.json' não encontrado em: {geojson_path}")
            st.stop()  # Para a execução do app se o arquivo não existir
            
        df_filtrado["codigo_ibge"] = df_filtrado["codigo_ibge"].astype(str)
        df_filtrado["Arrecadacao_hover"] = df_filtrado["Arrecadação"].apply(
            lambda x: f"R$ {x:,.0f}".replace(
                ",", ".") if pd.notna(x) else "R$ 0"
        )
        fig_mapa_03 = px.choropleth_mapbox(
            df_filtrado,
            geojson=geojson_mapa,
            locations="codigo_ibge",
            featureidkey="properties.id",
            hover_name="Município",
            custom_data=["Arrecadacao_hover"],
            mapbox_style="carto-positron",
            center={"lat": -10, "lon": -52},
            zoom=3.3,
            opacity=0.7,
            height=520
        )
        fig_mapa_03.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
            "<br>%{customdata[0]}<extra></extra>")
        fig_mapa_03.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        st.plotly_chart(fig_mapa_03, use_container_width=True, key="grafico_mapa_arrecadacao")

# ------------------------------------------------------------
# TAB 3 — RELATÓRIO PDF
# ------------------------------------------------------------
with tab3:
    st.subheader("Gerar Relatório")
    gerar = st.button("📄 Gerar Relatório em PDF")

    if gerar:
        msg = st.info("⏳ Gerando relatório, por favor aguarde...")
        try:
            pio.kaleido.scope.default_format = "png"
        except:
            pass

        styles = getSampleStyleSheet()
        story = []  # story definido aqui, dentro do if

        # ----- TÍTULO PDF -----
     #   logo = Image("IBGE.PNG", width=60, height=60)
     #   story.append(logo)
     #   story.append(Spacer(1, 1))

        story.append(Paragraph(
            "<b>Painel de Desenvolvimento Econômico e Turístico</b>",
            styles["Title"]
        ))

        data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M")
        styles.add(ParagraphStyle(
            name="DataDireita",
            parent=styles["Normal"],
            fontSize=8,
            alignment=TA_RIGHT
        ))

        story.append(Paragraph(
            f"Gerado em: {data_formatada}", styles["DataDireita"]
        ))
        story.append(Spacer(1, 12))

        # ----- TEXTO DE INTRODUÇÃO -----
        texto_intro = """
Este relatório foi desenvolvido para fornecer uma visão completa sobre o desempenho dos polos turísticos, empregos, estabelecimentos e o nível de engajamento de visitantes nos municípios.
A análise utiliza informações reais da base do IBGE, com o objetivo de avaliar tendências, padrões de comportamento e indicadores que influenciam a economia e o turismo local.
Este relatório apresenta gráficos e análises detalhadas para apoiar decisões estratégicas e políticas públicas.
"""
        story.append(Paragraph(texto_intro, styles["Normal"]))
        story.append(Spacer(1, 18))

        texto_emp = "Os resultados observados indicam diferenças na geração de empregos."
        texto_est = "A partir das informações levantadas, é possível identificar a quantidade de estabelecimentos turísticos."
        texto_vis = "As informações disponíveis evidenciam o total de visitas."
        texto_arr = "Os dados apresentados demonstram os valores de arrecadação registrados."

        texto_kpi = "Os principais indicadores econômicos e turísticos por município são apresentados abaixo:"
        story.append(Paragraph(texto_kpi, styles["Normal"]))
        story.append(Spacer(1, 18))

        # ----- KPIs lado a lado -----
        kpis = [
            ["Total de Empregos", f"{total_empregos:,}".replace(',', '.')],
            ["Estabelecimentos", f"{qtd_estabelecimentos:,}".replace(',', '.')],
            ["Visitas Nacionais", f"{visitas_nac:,}".replace(',', '.')],
            ["Visitas Internacionais", f"{visitas_int:,}".replace(',', '.')],
            ["Arrecadação", f"R$ {arrecadacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')]
        ]
        table_data = [[kpi[0] + "\n" + kpi[1] for kpi in kpis]]
        t = Table(table_data, colWidths=[1.5*inch]*5, hAlign='CENTER')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1C4D86")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white)
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        # ----- DICIONÁRIO DE SIGLAS -----
        sigla_para_estado = {
            "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
            "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
            "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
            "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
            "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
            "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
            "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
        }

        # ----- Funções para gerar markdowns -----
        def gerar_markdown_empregos(df):
            df_uf = df.groupby("Estado", as_index=False)["Empregos"].sum()
            markdown = ""
            for _, row in df_uf.iterrows():
                sigla = row["Estado"]
                estado = sigla_para_estado.get(sigla, sigla)
                empregos = f"{int(row['Empregos']):,}".replace(",", ".")
                markdown += f"Em **{estado}** foram gerados cerca de **{empregos} empregos**.\n"
            return markdown

        def gerar_markdown_estabelecimentos(df):
            df_uf = df.groupby("Estado", as_index=False)["Estabelecimentos"].sum()
            markdown = ""
            for _, row in df_uf.iterrows():
                sigla = row["Estado"]
                estado = sigla_para_estado.get(sigla, sigla)
                estabe = f"{int(row['Estabelecimentos']):,}".replace(",", ".")
                markdown += f"Em {estado}, contabilizam-se aproximadamente {estabe} estabelecimentos turísticos.\n"
            return markdown

        def gerar_markdown_visitas(df):
            df_visitas = df.groupby("Estado", as_index=False)[
                ["Visitas Nacionais", "Visitas Internacionais"]
            ].sum()
            markdown = ""
            for _, row in df_visitas.iterrows():
                sigla = row["Estado"]
                estado = sigla_para_estado.get(sigla, sigla)
                nac = f"{int(row['Visitas Nacionais']):,}".replace(",", ".")
                intl = f"{int(row['Visitas Internacionais']):,}".replace(",", ".")
                markdown += f"Em {estado}, contabilizaram-se {nac} visitas nacionais e {intl} visitas internacionais.\n"
            return markdown

        def gerar_markdown_arrecadacao(df):
            df_arrec = df.groupby("Estado", as_index=False)["Arrecadação"].sum()
            markdown = ""
            for _, row in df_arrec.iterrows():
                sigla = row["Estado"]
                estado = sigla_para_estado.get(sigla, sigla)
                valor = f"R$ {row['Arrecadação']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                markdown += f"No estado de {estado}, a arrecadação foi de aproximadamente {valor}.\n"
            return markdown

        # ----- Gerar markdowns -----
        markdown_empregos = gerar_markdown_empregos(df_filtrado)
        markdown_estabelecimentos = gerar_markdown_estabelecimentos(df_filtrado)
        markdown_visitas = gerar_markdown_visitas(df_filtrado)
        markdown_arrecadacao = gerar_markdown_arrecadacao(df_filtrado)

        titulo_menor = ParagraphStyle(
            name="TituloMenor",
            fontSize=14,
            leading=16,
            textColor=colors.black,
            spaceAfter=10
        )

        # ----- Função para salvar gráfico e inserir markdown -----
        def salvar_e_inserir(fig, titulo, descricao, markdown_dinamico=None):
            story.append(Paragraph(f"<b>{titulo}</b>", titulo_menor))
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                fig.write_image(tmp.name, scale=2)
                story.append(Image(tmp.name, width=5*inch, height=3.5*inch))
                story.append(Spacer(1, 1))
            except Exception as e:
                story.append(Paragraph(f"Erro ao salvar gráfico: {e}", styles["Normal"]))

            if descricao:
                story.append(Paragraph(descricao, styles["Normal"]))
                story.append(Spacer(1, 1))

            if markdown_dinamico:
                for linha in markdown_dinamico.split("\n"):
                    if linha.strip():
                        linha_formatada = linha.replace("**", "")
                        story.append(Paragraph(linha_formatada, styles["Normal"]))
                story.append(Spacer(1, 14))

        # ----- Inserir gráficos + markdowns -----
        salvar_e_inserir(fig_barras, "Quantidade de empregos por Estado",
                         texto_emp, markdown_empregos)
        salvar_e_inserir(fig_barras_02, "Quantidade de estabelecimentos turísticos por Estado",
                         texto_est, markdown_estabelecimentos)
        salvar_e_inserir(fig_barrasVisitas, "Comparação entre visitas nacionais e internacionais",
                         texto_vis, markdown_visitas)
        salvar_e_inserir(fig_linhas, "Evolução da arrecadação turística",
                         texto_arr, markdown_arrecadacao)

        # ----- Logo e assinatura -----
        #logo_final = Image("logo.png", width=60, height=60)
        #assinatura = Table([[ '', logo_final ]], colWidths=[400, 60])
        #assinatura.setStyle(TableStyle([
            #('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            #('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            #('ALIGN', (0, 0), (0, 0), 'LEFT')
        #]))
        #story.append(Spacer(1, 20))
        #story.append(assinatura)
        #story.append(Spacer(1, 20))

        # ----- Gerar PDF -----
        tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp_pdf.name, pagesize=A4)
        doc.build(story)

        with open(tmp_pdf.name, "rb") as f:
            pdf_bytes = f.read()

        st.success("PDF gerado com sucesso!")
        st.download_button(
            "⬇️ Baixar PDF",
            pdf_bytes,
            file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

# ------------------------------------------------------------
# Estilo do Dashboard
# ------------------------------------------------------------
st.markdown("""
<style>

/* Fundo geral com degradê */
html, body {
    background: linear-gradient(135deg, #DDE7F0 0%, #AFC8E4 40%, #1C4D86 100%) !important;
    height: 100%;
    margin: 0;
    padding: 0;
}

/* Deixar TUDO transparente para mostrar o degradê */
.stApp, .block-container, .st-emotion-cache-12fmjuu, section.main {
    background: transparent !important;
}

/* Sidebar com sombra lateral */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0) !important;
    backdrop-filter: blur(6px);  
    box-shadow: 8px 0 18px rgba(0,0,0,0.25);  /* SOMBRA lateral da esquerda para a direita */
    z-index: 10;
}

/* Cabeçalho/toolbar do deploy */
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0) !important;
}

/* Footer transparente */
footer, .stFooter {
    background: rgba(0, 0, 0, 0) !important;
}

/* Conteúdo com leve sombra */
.block-container {
    box-shadow: 0 0 22px rgba(0,0,0,0.18);
    border-radius: 12px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)
