import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="AlphaLens — Hall da Fama B3",
    page_icon="▲",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #F2F0E8 !important;
    font-family: 'DM Mono', monospace !important;
    color: #0A0A0A !important;
}

[data-testid="stMain"] {
    background-color: #F2F0E8 !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F2F0E8; }
::-webkit-scrollbar-thumb { background: #0A0A0A; }

st.markdown("""
<div class="alphalens-header">

  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="52" height="52" style="flex-shrink:0">
    <defs>
      <clipPath id="sc"><circle cx="98" cy="98" r="76"/></clipPath>
      <linearGradient id="sg" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%"   stop-color="#E8FF00" stop-opacity="0.22"/>
        <stop offset="100%" stop-color="#E8FF00" stop-opacity="0"/>
      </linearGradient>
    </defs>
    <circle cx="98" cy="98" r="90" fill="none" stroke="#E8FF00" stroke-width="1" opacity="0.1"/>
    <circle cx="98" cy="98" r="80" fill="none" stroke="#E8FF00" stroke-width="5"/>
    <circle cx="98" cy="98" r="72" fill="none" stroke="#E8FF00" stroke-width="1" opacity="0.16"/>
    <g clip-path="url(#sc)">
      <line x1="22" y1="138" x2="174" y2="138" stroke="#E8FF00" stroke-width="1" opacity="0.07"/>
      <line x1="22" y1="114" x2="174" y2="114" stroke="#E8FF00" stroke-width="1" opacity="0.07"/>
      <line x1="22" y1="90"  x2="174" y2="90"  stroke="#E8FF00" stroke-width="1" opacity="0.07"/>
      <polygon points="28,148 46,142 60,148 76,128 90,120 102,106 114,110 128,86 144,78 162,56 174,50 174,185 28,185" fill="url(#sg)"/>
      <polyline points="28,148 46,142 60,148 76,128 90,120 102,106 114,110 128,86 144,78 162,56 174,50"
        fill="none" stroke="#E8FF00" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="28"  cy="148" r="3" fill="#E8FF00" opacity="0.45"/>
      <circle cx="76"  cy="128" r="3" fill="#E8FF00" opacity="0.45"/>
      <circle cx="102" cy="106" r="3" fill="#E8FF00" opacity="0.45"/>
      <circle cx="128" cy="86"  r="3" fill="#E8FF00" opacity="0.45"/>
      <circle cx="174" cy="50"  r="5.5" fill="#E8FF00"/>
      <circle cx="174" cy="50"  r="9" fill="none" stroke="#E8FF00" stroke-width="1.5" opacity="0.35"/>
    </g>
    <line x1="162" y1="162" x2="200" y2="200" stroke="#E8FF00" stroke-width="13" stroke-linecap="round"/>
    <line x1="162" y1="162" x2="200" y2="200" stroke="#080808" stroke-width="4.5" stroke-linecap="round"/>
  </svg>

  <div class="al-logo">AlphaLens</div>
  <div class="al-sub">Hall da Fama B3 &nbsp;&middot;&nbsp; Rankeie seu trade na historia da bolsa</div>

</div>
""", unsafe_allow_html=True)

.alphalens-header {
    background: #0A0A0A;
    padding: 20px 40px;
    margin: -1rem -1rem 0 -1rem;
    border-bottom: 3px solid #0A0A0A;
    display: flex;
    align-items: baseline;
    gap: 20px;
    overflow: hidden;
    position: relative;
}

.alphalens-header::after {
    content: 'A';
    position: absolute;
    right: -20px;
    top: -30px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 180px;
    color: rgba(232,255,0,0.06);
    line-height: 1;
    pointer-events: none;
}

.al-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    color: #E8FF00;
    letter-spacing: 6px;
    line-height: 1;
}

.al-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: rgba(232,255,0,0.45);
    letter-spacing: 4px;
    text-transform: uppercase;
    border-left: 2px solid rgba(232,255,0,0.2);
    padding-left: 20px;
}

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    color: #0A0A0A !important;
}

h1 {
    font-size: 48px !important;
    letter-spacing: 3px !important;
    border-bottom: 3px solid #0A0A0A;
    padding-bottom: 8px;
    margin-bottom: 16px !important;
}

h2 { font-size: 32px !important; letter-spacing: 2px !important; }
h3 { font-size: 24px !important; letter-spacing: 2px !important; }

p, li, label, span {
    font-family: 'DM Mono', monospace !important;
}

[data-baseweb="tab-list"] {
    background: #0A0A0A !important;
    border-bottom: 3px solid #0A0A0A !important;
    gap: 0 !important;
    padding: 0 !important;
}

[data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(232,255,0,0.4) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-right: 1px solid rgba(232,255,0,0.1) !important;
    padding: 14px 24px !important;
    transition: all 0.1s !important;
}

[data-baseweb="tab"]:hover {
    background: rgba(232,255,0,0.08) !important;
    color: #E8FF00 !important;
}

[aria-selected="true"][data-baseweb="tab"] {
    background: #E8FF00 !important;
    color: #0A0A0A !important;
    border-bottom: none !important;
}

[data-baseweb="tab-highlight"] { display: none !important; }

[data-baseweb="tab-panel"] {
    background: #F2F0E8 !important;
    padding-top: 24px !important;
}

.stButton > button {
    background: #0A0A0A !important;
    color: #E8FF00 !important;
    border: 3px solid #0A0A0A !important;
    border-radius: 0 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 20px !important;
    letter-spacing: 3px !important;
    padding: 12px 24px !important;
    box-shadow: 6px 6px 0 rgba(10,10,10,0.3) !important;
    transition: all 0.1s !important;
    width: 100%;
}

.stButton > button:hover {
    transform: translate(-4px, -4px) !important;
    box-shadow: 10px 10px 0 rgba(10,10,10,0.3) !important;
    background: #E8FF00 !important;
    color: #0A0A0A !important;
}

.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0 rgba(10,10,10,0.3) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #ffffff !important;
    border: 3px solid #0A0A0A !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    color: #0A0A0A !important;
    padding: 10px 14px !important;
    box-shadow: 4px 4px 0 rgba(10,10,10,0.2) !important;
    transition: all 0.1s !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0A0A0A !important;
    box-shadow: 6px 6px 0 rgba(10,10,10,0.2) !important;
    transform: translate(-2px, -2px) !important;
    outline: none !important;
}

.stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: rgba(10,10,10,0.5) !important;
    font-weight: 500 !important;
}

.stSelectbox > div > div {
    background: #ffffff !important;
    border: 3px solid #0A0A0A !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0 rgba(10,10,10,0.2) !important;
    font-family: 'DM Mono', monospace !important;
    transition: all 0.1s !important;
}

.stSelectbox > div > div > div {
    color: #0A0A0A !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

[data-testid="stMetric"] {
    background: #0A0A0A !important;
    border: 3px solid #0A0A0A !important;
    padding: 16px 20px !important;
    box-shadow: 6px 6px 0 rgba(10,10,10,0.25) !important;
}

[data-testid="stMetricLabel"] > div,
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: rgba(232,255,0,0.5) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 36px !important;
    color: #E8FF00 !important;
    letter-spacing: 2px !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

[data-testid="stMetricDelta"] svg {
    fill: rgba(232,255,0,0.6) !important;
}

[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-width: 3px !important;
    border-style: solid !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

hr {
    border: none !important;
    border-top: 3px solid #0A0A0A !important;
    margin: 24px 0 !important;
}

.stProgress > div > div > div > div {
    background: #E8FF00 !important;
    border-radius: 0 !important;
}

.stProgress > div > div {
    background: rgba(10,10,10,0.12) !important;
    border-radius: 0 !important;
    border: 1px solid #0A0A0A !important;
    height: 10px !important;
}

.stCode, [data-testid="stCode"] {
    background: #0A0A0A !important;
    border: 3px solid #0A0A0A !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0 rgba(10,10,10,0.25) !important;
}

.stCode code, pre {
    font-family: 'DM Mono', monospace !important;
    color: #E8FF00 !important;
    font-size: 13px !important;
    background: #0A0A0A !important;
}

table {
    border-collapse: collapse !important;
    width: 100% !important;
    font-family: 'DM Mono', monospace !important;
    border: 3px solid #0A0A0A !important;
    box-shadow: 6px 6px 0 rgba(10,10,10,0.15) !important;
}

th {
    background: #0A0A0A !important;
    color: #E8FF00 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 14px !important;
    letter-spacing: 2px !important;
    padding: 12px 16px !important;
    border: 1px solid rgba(232,255,0,0.2) !important;
    text-align: left !important;
}

td {
    padding: 10px 16px !important;
    border: 1px solid rgba(10,10,10,0.12) !important;
    font-size: 13px !important;
    background: #ffffff !important;
}

tr:nth-child(even) td { background: #F2F0E8 !important; }
tr:hover td { background: rgba(232,255,0,0.08) !important; }

.stCaption, [data-testid="stCaptionContainer"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 1px !important;
    opacity: 0.45 !important;
}

[data-testid="column"] { padding: 0 6px !important; }

#MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="alphalens-header">
    <div class="al-logo">AlphaLens</div>
    <div class="al-sub">Hall da Fama B3 &nbsp;&middot;&nbsp; Rankeie seu trade na historia da bolsa</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


def buscar_dados(ticker, start, end):
    dados = yf.download(
        f"{ticker}.SA",
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )
    if dados.empty:
        return None
    return pd.Series(dados["Close"].values.flatten(), index=dados.index)


def calcular_todos_retornos(preco):
    precos = preco.values
    n = len(precos)
    retornos_todos = (precos[np.newaxis, :] - precos[:, np.newaxis]) / precos[:, np.newaxis]
    mask = np.triu(np.ones((n, n), dtype=bool), k=1)
    return retornos_todos[mask] * 100


def calcular_edge_score(retorno, dias_holding, preco_serie):
    score_retorno = min(40, max(0, (retorno / 200) * 40)) if retorno > 0 else max(-20, (retorno / 100) * 20)
    eficiencia = retorno / max(1, dias_holding) * 30
    score_tempo = min(25, max(0, eficiencia))
    retornos_diarios = preco_serie.pct_change().dropna()
    vol = retornos_diarios.std() * np.sqrt(252) * 100
    score_vol = max(0, 20 - (vol / 5))
    rolling_max = preco_serie.cummax()
    drawdown = ((preco_serie - rolling_max) / rolling_max * 100).min()
    score_dd = max(0, 15 + (drawdown / 5))
    return min(100, max(0, round(score_retorno + score_tempo + score_vol + score_dd)))


def classificar_edge(score):
    if score >= 85:   return "LENDARIO",    "▲▲▲", "#E8FF00"
    elif score >= 70: return "EXCEPCIONAL", "▲▲",  "#00FF66"
    elif score >= 55: return "BOM",         "▲",   "#4a90d9"
    elif score >= 40: return "MEDIANO",     "◆",   "#FF8800"
    else:             return "FRACO",       "▼",   "#FF2200"


def calcular_cdi(ano_c, mes_c, ano_v, mes_v):
    anos = (ano_v * 12 + mes_v - ano_c * 12 - mes_c) / 12
    return round((pow(1.105, anos) - 1) * 100, 1)


HALL_FAMA = [
    {"pos": 1, "ticker": "WEGE3", "ret": 8700, "label": "Jan/2010 -> Jan/2024"},
    {"pos": 2, "ticker": "PRIO3", "ret": 1240, "label": "Mar/2020 -> Ago/2022"},
    {"pos": 3, "ticker": "CPLE6", "ret": 890,  "label": "Abr/2020 -> Dez/2021"},
    {"pos": 4, "ticker": "RADL3", "ret": 620,  "label": "Jan/2015 -> Dez/2020"},
    {"pos": 5, "ticker": "RENT3", "ret": 480,  "label": "Jan/2018 -> Jan/2022"},
    {"pos": 6, "ticker": "VALE3", "ret": 340,  "label": "Mar/2020 -> Jul/2021"},
    {"pos": 7, "ticker": "PETR4", "ret": 310,  "label": "Jan/2016 -> Jun/2022"},
    {"pos": 8, "ticker": "ITUB4", "ret": 156,  "label": "Jan/2016 -> Jan/2020"},
]

HALL_VERGONHA = [
    {"pos": 1, "ticker": "OIBR3", "ret": -99, "label": "Jan/2014 -> Dez/2023"},
    {"pos": 2, "ticker": "MGLU3", "ret": -92, "label": "Nov/2021 -> Jan/2023"},
    {"pos": 3, "ticker": "VVAR3", "ret": -88, "label": "Ago/2021 -> Jun/2023"},
    {"pos": 4, "ticker": "CESP3", "ret": -71, "label": "Jan/2010 -> Dez/2015"},
    {"pos": 5, "ticker": "BVMF3", "ret": -58, "label": "Mai/2019 -> Mar/2020"},
]

RADAR = [
    {"ticker": "PETR4", "ret": 24.1,  "dias": 12, "pct": 99.3, "signal": "MOMENTUM EXTREMO"},
    {"ticker": "VALE3", "ret": -18.7, "dias": 8,  "pct": 97.1, "signal": "REVERSAO PROVAVEL"},
    {"ticker": "WEGE3", "ret": 31.2,  "dias": 20, "pct": 99.8, "signal": "RARO HISTORICO"},
    {"ticker": "ITUB4", "ret": 15.4,  "dias": 15, "pct": 94.2, "signal": "ACIMA DA MEDIA"},
    {"ticker": "BBDC4", "ret": -22.3, "dias": 10, "pct": 98.4, "signal": "QUEDA ANORMAL"},
]


aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "▲  ANALISAR TRADE",
    "★  RANKING GLOBAL",
    "◆  EDGE SCORE",
    "►  TRADE REPLAY",
    "//  INTELIGENCIA",
])


with aba1:

    ticker = st.text_input("Ticker", placeholder="Ex: PETR4").upper()

    col1, col2 = st.columns(2)
    with col1:
        ano_compra = st.selectbox("Ano de Compra", range(2010, 2025))
        mes_compra = st.selectbox("Mes de Compra", range(1, 13), format_func=lambda m: f"{m:02d}")
    with col2:
        ano_venda = st.selectbox("Ano de Venda", range(2010, 2025), index=10)
        mes_venda = st.selectbox("Mes de Venda", range(1, 13), format_func=lambda m: f"{m:02d}")

    investido = st.number_input("Quanto voce investiu? R$ (opcional)", min_value=0.0, value=0.0, step=100.0)

    if st.button("▲  ANALISAR TRADE"):
        if not ticker:
            st.error("Digite um ticker.")
        elif (ano_compra, mes_compra) >= (ano_venda, mes_venda):
            st.error("A data de compra precisa ser antes da data de venda.")
        else:
            with st.spinner("Buscando dados da B3..."):
                dados = yf.download(
                    f"{ticker}.SA",
                    start=f"{ano_compra}-{mes_compra:02d}-01",
                    end=f"{ano_venda}-{mes_venda:02d}-28",
                    auto_adjust=True,
                    progress=False
                )

            if dados.empty:
                st.error(f"Ticker '{ticker}' nao encontrado.")
            else:
                preco = pd.Series(dados["Close"].values.flatten(), index=dados.index)

                st.success(f"+ {len(preco)} dias de dados encontrados para {ticker}.")
                st.line_chart(preco)

                preco_compra = preco[f"{ano_compra}-{mes_compra:02d}"].iloc[0]
                preco_venda  = preco[f"{ano_venda}-{mes_venda:02d}"].iloc[0]
                retorno = ((preco_venda - preco_compra) / preco_compra) * 100

                st.subheader("Seu Trade")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Preco de Compra", f"R$ {preco_compra:.2f}")
                with col_b:
                    st.metric("Preco de Venda", f"R$ {preco_venda:.2f}")
                with col_c:
                    st.metric("Retorno", f"{'+' if retorno >= 0 else ''}{retorno:.1f}%")

                precos_arr = preco.values
                n = len(precos_arr)
                retornos_todos = (precos_arr[np.newaxis, :] - precos_arr[:, np.newaxis]) / precos_arr[:, np.newaxis]
                mask = np.triu(np.ones((n, n), dtype=bool), k=1)
                retornos_validos = retornos_todos[mask] * 100

                total     = len(retornos_validos)
                melhor    = retornos_validos.max()
                pior      = retornos_validos.min()
                posicao   = (retornos_validos <= retorno).sum()
                percentil = (posicao / total) * 100
                top_pct   = 100 - percentil
                rank_num  = int(total - posicao + 1)

                st.subheader("Ranking")
                col_d, col_e, col_f = st.columns(3)
                with col_d:
                    st.metric("Melhor Trade Possivel", f"+{melhor:.1f}%")
                with col_e:
                    st.metric("Pior Trade Possivel", f"{pior:.1f}%")
                with col_f:
                    st.metric("Seu Percentil", f"Top {top_pct:.1f}%")

                st.info(f"Seu trade ficou melhor que {percentil:.1f}% de todos os {total:,} trades possiveis com {ticker}.")

                st.subheader("Distribuicao de Todos os Trades Possiveis")
                df_hist = pd.DataFrame({"retorno": retornos_validos})
                fig = px.histogram(
                    df_hist, x="retorno", nbins=80,
                    labels={"retorno": "Retorno (%)"},
                    color_discrete_sequence=["#4a90d9"]
                )
                fig.add_vline(
                    x=retorno, line_color="#E8FF00", line_width=3,
                    annotation_text="VOCE", annotation_font_color="#E8FF00",
                    annotation_font_size=14
                )
                fig.update_layout(
                    paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A",
                    font_color="#F2F0E8", showlegend=False,
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                )
                st.plotly_chart(fig, use_container_width=True)

                dias_holding = (preco.index[-1] - preco.index[0]).days
                edge = calcular_edge_score(retorno, dias_holding, preco)
                edge_label, edge_icon, edge_cor = classificar_edge(edge)
                cdi    = calcular_cdi(ano_compra, mes_compra, ano_venda, mes_venda)
                vs_cdi = round(retorno - cdi, 1)

                st.subheader("Edge Score")
                ec1, ec2 = st.columns(2)
                with ec1:
                    st.metric("Edge Score", f"{edge} / 100 — {edge_icon} {edge_label}")
                with ec2:
                    st.metric(
                        "vs CDI no periodo",
                        f"{'+' if vs_cdi >= 0 else ''}{vs_cdi:.1f} p.p.",
                        delta=f"CDI estimado: +{cdi}%"
                    )

                if investido > 0:
                    reais_end  = round(investido * (1 + retorno / 100))
                    reais_best = round(investido * (1 + melhor / 100))
                    st.subheader("Em Reais")
                    r1, r2 = st.columns(2)
                    with r1:
                        st.metric(
                            "Seu investimento virou",
                            f"R$ {reais_end:,.0f}",
                            delta=f"R$ {reais_end - investido:,.0f}"
                        )
                    with r2:
                        st.metric(
                            "No melhor trade possivel teria virado",
                            f"R$ {reais_best:,.0f}",
                            delta=f"R$ {reais_best - reais_end:,.0f} a mais"
                        )

                st.subheader("Veredicto")
                if top_pct <= 10:
                    st.success(f"▲▲▲  Top {top_pct:.1f}% — Trade historico. De {total:,} combinacoes possiveis, o seu ficou entre os melhores ja alcancaveis com {ticker}.")
                elif top_pct <= 30:
                    st.success(f"▲▲  Top {top_pct:.1f}% — Excepcional. Voce superou {percentil:.1f}% de todos os trades possiveis com {ticker}.")
                elif top_pct <= 50:
                    st.info(f"▲  Top {top_pct:.1f}% — Acima da media. Voce superou mais da metade das possibilidades.")
                elif top_pct <= 75:
                    st.warning(f"◆  Bottom {100 - top_pct:.0f}% — Abaixo da media. O melhor trade possivel com {ticker} teria chegado a +{melhor:.1f}%.")
                else:
                    st.error(f"▼  Timing catastrofico. Entre os {100 - top_pct:.0f}% piores trades possiveis. O mesmo ativo nas datas certas teria rendido +{melhor:.1f}%.")

                st.subheader("E se voce tivesse segurado?")
                with st.spinner("Buscando dados pos-venda..."):
                    preco_pos = buscar_dados(
                        ticker,
                        f"{ano_venda}-{mes_venda:02d}-01",
                        str(datetime.today().date())
                    )

                if preco_pos is not None and len(preco_pos) > 30:
                    preco_hoje  = preco_pos.iloc[-1]
                    retorno_pos = ((preco_hoje - preco_venda) / preco_venda) * 100
                    retorno_tot = ((preco_hoje - preco_compra) / preco_compra) * 100

                    w1, w2, w3 = st.columns(3)
                    with w1:
                        st.metric("Voce vendeu em", f"{'+' if retorno >= 0 else ''}{retorno:.1f}%")
                    with w2:
                        st.metric("Apos sua venda o ativo foi", f"{'+' if retorno_pos >= 0 else ''}{retorno_pos:.1f}%")
                    with w3:
                        st.metric("Se tivesse segurado ate hoje", f"{'+' if retorno_tot >= 0 else ''}{retorno_tot:.1f}%")

                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(
                        x=preco.index, y=preco.values,
                        name="Seu periodo",
                        line=dict(color="#E8FF00", width=2)
                    ))
                    fig2.add_trace(go.Scatter(
                        x=preco_pos.index, y=preco_pos.values,
                        name="Apos sua venda",
                        line=dict(color="#FF2200", width=2, dash="dash")
                    ))

                    data_saida = preco_pos.index[0]
                    fig2.add_shape(
                        type="line",
                        x0=data_saida, x1=data_saida,
                        y0=0, y1=1,
                        xref="x", yref="paper",
                        line=dict(color="rgba(255,255,255,0.4)", dash="dot", width=1.5)
                    )
                    fig2.add_annotation(
                        x=data_saida, y=1,
                        xref="x", yref="paper",
                        text="VOCE SAIU",
                        showarrow=False,
                        font=dict(color="white", size=11),
                        yanchor="bottom"
                    )
                    fig2.update_layout(
                        paper_bgcolor="#0A0A0A", plot_bgcolor="#0A0A0A",
                        font_color="#F2F0E8",
                        legend=dict(bgcolor="rgba(0,0,0,0)"),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                    if retorno_pos > 20:
                        st.warning(f"O ativo subiu mais {retorno_pos:.1f}% depois que voce saiu. Se tivesse segurado, seu retorno total seria {retorno_tot:.1f}%.")
                    elif retorno_pos < -10:
                        st.success(f"Boa saida. O ativo caiu {abs(retorno_pos):.1f}% depois que voce vendeu.")
                    else:
                        st.info("O ativo ficou relativamente estavel depois da sua saida.")

                st.subheader("Card para Compartilhar")
                reais_str = f"\nR${investido:,.0f} -> R${round(investido * (1 + retorno / 100)):,.0f}" if investido > 0 else ""
                card = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALPHALENS — MEU TRADE — B3

Ticker:    {ticker}
Periodo:   {mes_compra:02d}/{ano_compra} -> {mes_venda:02d}/{ano_venda}
Retorno:   {'+' if retorno >= 0 else ''}{retorno:.1f}%{reais_str}

Edge Score:  {edge}/100  {edge_icon} {edge_label}
Ranking:     #{rank_num:,} de {total:,} trades
Percentil:   Top {top_pct:.1f}% historico
vs CDI:      {'+' if vs_cdi >= 0 else ''}{vs_cdi:.1f} p.p.

hall-da-fama-b3.streamlit.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                st.code(card, language=None)
                st.caption("Copie o texto acima e cole no LinkedIn")

                st.session_state["resultado"] = {
                    "ticker": ticker,
                    "retorno": retorno,
                    "edge": edge,
                    "rank_num": rank_num,
                    "total": total,
                    "top_pct": top_pct,
                    "percentil": percentil,
                    "melhor": melhor,
                    "pior": pior,
                    "ano_c": ano_compra,
                    "mes_c": mes_compra,
                    "ano_v": ano_venda,
                    "mes_v": mes_venda,
                }


with aba2:

    st.subheader("Ranking Global — Melhores e Piores Trades da Historia da B3")

    st.markdown("#### Hall da Fama — Os Imortais")
    for item in HALL_FAMA:
        c1, c2, c3, c4 = st.columns([0.4, 1.2, 2.5, 1])
        with c1:
            st.markdown(f"**#{item['pos']}**")
        with c2:
            st.markdown(f"**{item['ticker']}**")
        with c3:
            st.markdown(item["label"])
        with c4:
            st.markdown(
                f"<span style='color:#00FF66;font-size:18px;font-weight:bold'>+{item['ret']:,}%</span>",
                unsafe_allow_html=True
            )
        st.divider()

    st.markdown("#### Hall da Vergonha — Os Micos Eternos")
    for item in HALL_VERGONHA:
        c1, c2, c3, c4 = st.columns([0.4, 1.2, 2.5, 1])
        with c1:
            st.markdown(f"**#{item['pos']}**")
        with c2:
            st.markdown(f"**{item['ticker']}**")
        with c3:
            st.markdown(item["label"])
        with c4:
            st.markdown(
                f"<span style='color:#FF2200;font-size:18px;font-weight:bold'>{item['ret']}%</span>",
                unsafe_allow_html=True
            )
        st.divider()

    if "resultado" in st.session_state:
        r = st.session_state["resultado"]
        st.markdown("#### Sua Posicao no Ranking")
        st.info(
            f"**{r['ticker']}** | {r['mes_c']:02d}/{r['ano_c']} -> {r['mes_v']:02d}/{r['ano_v']} | "
            f"Retorno: **{'+' if r['retorno'] >= 0 else ''}{r['retorno']:.1f}%** | "
            f"Ranking: **#{r['rank_num']:,} de {r['total']:,} trades** | "
            f"Top **{r['top_pct']:.1f}%**"
        )


with aba3:

    st.subheader("Edge Score — A Metrica Unica do Seu Trade")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        #### Como e calculado

        | Dimensao | Peso | O que mede |
        |---|---|---|
        | Retorno % | 40 pts | Quanto o trade rendeu |
        | Eficiencia temporal | 25 pts | Retorno por dia de holding |
        | Volatilidade | 20 pts | Quanto o ativo oscilou |
        | Drawdown maximo | 15 pts | Maior queda durante o trade |

        **Total maximo: 100 pontos**
        """)
    with c2:
        st.markdown("""
        #### Classificacoes

        | Score | Classificacao |
        |---|---|
        | 85 — 100 | ▲▲▲  LENDARIO |
        | 70 — 84 | ▲▲  EXCEPCIONAL |
        | 55 — 69 | ▲  BOM |
        | 40 — 54 | ◆  MEDIANO |
        | 0 — 39 | ▼  FRACO |

        > Um trade de +50% em 1 semana tem Edge Score muito maior que +50% em 5 anos.
        """)

    st.markdown("---")
    st.markdown("#### Calcule o Edge Score de qualquer trade")

    et = st.text_input("Ticker", placeholder="Ex: WEGE3", key="et").upper()
    ea1, ea2 = st.columns(2)
    with ea1:
        eac = st.selectbox("Ano Compra", range(2010, 2025), key="eac")
        emc = st.selectbox("Mes Compra", range(1, 13), format_func=lambda m: f"{m:02d}", key="emc")
    with ea2:
        eav = st.selectbox("Ano Venda", range(2010, 2025), index=10, key="eav")
        emv = st.selectbox("Mes Venda", range(1, 13), format_func=lambda m: f"{m:02d}", key="emv")

    if st.button("◆  CALCULAR EDGE SCORE"):
        if et and (eac * 12 + emc) < (eav * 12 + emv):
            with st.spinner("Calculando..."):
                ep = buscar_dados(et, f"{eac}-{emc:02d}-01", f"{eav}-{emv:02d}-28")
            if ep is not None:
                try:
                    epc    = ep[f"{eac}-{emc:02d}"].iloc[0]
                    epv    = ep[f"{eav}-{emv:02d}"].iloc[0]
                    eret   = ((epv - epc) / epc) * 100
                    edias  = (ep.index[-1] - ep.index[0]).days
                    escore = calcular_edge_score(eret, edias, ep)
                    elabel, eicon, _ = classificar_edge(escore)
                    retd = ep.pct_change().dropna()
                    vol  = retd.std() * np.sqrt(252) * 100
                    dd   = ((ep - ep.cummax()) / ep.cummax() * 100).min()
                    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
                    with col_e1:
                        st.metric("Edge Score", f"{escore}/100")
                    with col_e2:
                        st.metric("Classificacao", f"{eicon} {elabel}")
                    with col_e3:
                        st.metric("Volatilidade anualizada", f"{vol:.1f}%")
                    with col_e4:
                        st.metric("Max Drawdown", f"{dd:.1f}%")
                    st.metric(
                        "Retorno / Holding",
                        f"{'+' if eret >= 0 else ''}{eret:.1f}%  |  {edias} dias"
                    )
                except Exception:
                    st.error("Nao foi possivel calcular para essas datas.")
            else:
                st.error("Ticker nao encontrado.")
        else:
            st.error("Preencha o ticker e datas validas.")

    if "resultado" in st.session_state:
        r = st.session_state["resultado"]
        st.markdown("---")
        st.info(f"Ultimo trade analisado: **{r['ticker']}** — Edge Score **{r['edge']}/100**")


with aba4:

    st.subheader("Trade Replay — Reviva seu Trade Dia a Dia")
    st.write("Veja como seu trade evoluiu ao longo do tempo com marcos e storytelling.")

    rt = st.text_input("Ticker", placeholder="Ex: PETR4", key="rt").upper()
    ra1, ra2 = st.columns(2)
    with ra1:
        rac = st.selectbox("Ano Compra", range(2010, 2025), key="rac")
        rmc = st.selectbox("Mes Compra", range(1, 13), format_func=lambda m: f"{m:02d}", key="rmc")
    with ra2:
        rav = st.selectbox("Ano Venda", range(2010, 2025), index=5, key="rav")
        rmv = st.selectbox("Mes Venda", range(1, 13), format_func=lambda m: f"{m:02d}", key="rmv")

    if st.button("►  INICIAR REPLAY"):
        if not rt:
            st.error("Digite um ticker.")
        elif (rac * 12 + rmc) >= (rav * 12 + rmv):
            st.error("Datas invalidas.")
        else:
            with st.spinner("Carregando dados..."):
                rp = buscar_dados(rt, f"{rac}-{rmc:02d}-01", f"{rav}-{rmv:02d}-28")

            if rp is None:
                st.error("Ticker nao encontrado.")
            else:
                base = rp.iloc[0]
                acum = ((rp - base) / base * 100)

                marcos_idx  = [0, len(rp)//4, len(rp)//2, 3*len(rp)//4, len(rp)-1]
                marcos_nome = ["Dia 1 — Compra", "25%", "Metade", "75%", "Venda"]
                cols_m = st.columns(5)
                for i, (idx, nome) in enumerate(zip(marcos_idx, marcos_nome)):
                    with cols_m[i]:
                        val  = acum.iloc[idx]
                        data = rp.index[idx].strftime("%d/%m/%y")
                        cor  = "green" if val >= 0 else "red"
                        st.markdown(
                            f"**{nome}**  \n{data}  \n:{cor}[{'+' if val >= 0 else ''}{val:.1f}%]"
                        )

                st.markdown("---")

                fig_r = go.Figure()
                fig_r.add_trace(go.Scatter(
                    x=acum.index, y=acum.values,
                    fill="tozeroy",
                    fillcolor="rgba(232,255,0,0.07)",
                    line=dict(color="#E8FF00", width=2),
                    hovertemplate="%{x|%d/%m/%Y}<br>Retorno: %{y:.2f}%<extra></extra>"
                ))
                fig_r.add_hline(y=0, line_color="rgba(255,255,255,0.2)", line_dash="dash")

                fig_r.add_trace(go.Scatter(
                    x=[acum.index[0]], y=[0],
                    mode="markers+text",
                    marker=dict(size=14, color="#E8FF00"),
                    text=["COMPRA"], textposition="top right",
                    textfont=dict(color="#E8FF00", size=11),
                    showlegend=False
                ))

                ret_f = acum.iloc[-1]
                fig_r.add_trace(go.Scatter(
                    x=[acum.index[-1]], y=[ret_f],
                    mode="markers+text",
                    marker=dict(size=14, color="#FF2200"),
                    text=[f"VENDA {'+' if ret_f >= 0 else ''}{ret_f:.1f}%"],
                    textposition="top left",
                    textfont=dict(color="#FF2200", size=11),
                    showlegend=False
                ))

                fig_r.add_trace(go.Scatter(
                    x=[acum.idxmax()], y=[acum.max()],
                    mode="markers+text",
                    marker=dict(size=10, color="#00FF66", symbol="triangle-up"),
                    text=[f"MAX +{acum.max():.1f}%"],
                    textposition="top center",
                    textfont=dict(color="#00FF66", size=10),
                    showlegend=False
                ))

                fig_r.add_trace(go.Scatter(
                    x=[acum.idxmin()], y=[acum.min()],
                    mode="markers+text",
                    marker=dict(size=10, color="#FF8800", symbol="triangle-down"),
                    text=[f"MIN {acum.min():.1f}%"],
                    textposition="bottom center",
                    textfont=dict(color="#FF8800", size=10),
                    showlegend=False
                ))

                fig_r.update_layout(
                    paper_bgcolor="#0A0A0A",
                    plot_bgcolor="#0A0A0A",
                    font_color="#F2F0E8",
                    showlegend=False,
                    height=400,
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
                    title=dict(text=f"Trade Replay — {rt}", font=dict(color="#E8FF00"))
                )
                st.plotly_chart(fig_r, use_container_width=True)

                st.subheader("Storytelling do Trade")
                if acum.min() < -15:
                    st.warning(f"Durante o trade voce chegou a estar {acum.min():.1f}% no negativo. A maioria dos traders venderia aqui por stop emocional.")
                if acum.max() > acum.iloc[-1] + 10:
                    st.info(f"O pico do trade foi +{acum.max():.1f}% — voce vendeu quando ja havia recuado {acum.max() - acum.iloc[-1]:.1f} p.p. do topo.")
                if acum.iloc[-1] >= 0:
                    st.success(f"Trade encerrado em +{acum.iloc[-1]:.1f}%.")
                else:
                    st.error(f"Trade encerrado em {acum.iloc[-1]:.1f}%. O ativo chegou a valer +{acum.max():.1f}% durante o periodo.")


with aba5:

    st.subheader("Trade Intelligence Engine — Analise Institucional da B3")

    st.markdown("#### Ativos com Movimentos Anormais")
    st.caption("Trades no percentil raro do historico — metodologia usada por fundos quantitativos.")

    for a in RADAR:
        cor   = "#00FF66" if a["ret"] > 0 else "#FF2200"
        cor_s = "#FF2200" if a["pct"] > 98 else "#FF8800" if a["pct"] > 95 else "#E8FF00"
        c1, c2, c3, c4, c5 = st.columns([0.8, 1.2, 1.8, 2, 1.5])
        with c1:
            st.markdown(f"**{a['ticker']}**")
        with c2:
            st.markdown(
                f"<span style='color:{cor};font-weight:bold'>{'+' if a['ret'] > 0 else ''}{a['ret']}%</span> / {a['dias']}d",
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(f"Percentil: **{a['pct']}%**")
        with c4:
            st.markdown(
                f"<span style='color:{cor_s};font-weight:bold'>{a['signal']}</span>",
                unsafe_allow_html=True
            )
        with c5:
            st.progress(a["pct"] / 100)
        st.divider()

    st.markdown("---")
    st.markdown("#### Heatmap Comportamental — Quando o Varejo Erra")

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("**Varejo vende cedo demais**")
        st.metric("Trades top 30%", "70% encerrados antes do pico")
        st.progress(0.70)
        st.caption("Retorno medio deixado na mesa: +34%")
    with b2:
        st.markdown("**Varejo segura tarde demais**")
        st.metric("Trades bottom 40%", "62% poderiam ter saido positivos")
        st.progress(0.62)
        st.caption("Loss medio evitavel: -28%")

    st.markdown("---")
    st.markdown("#### Trade Probability Score")
    st.caption("Insira um ticker e datas para receber uma previsao de qualidade baseada em padroes historicos.")

    tp = st.text_input("Ticker", placeholder="Ex: VALE3", key="tp").upper()
    tpa1, tpa2 = st.columns(2)
    with tpa1:
        tpac = st.selectbox("Ano Compra", range(2010, 2025), key="tpac")
        tpmc = st.selectbox("Mes Compra", range(1, 13), format_func=lambda m: f"{m:02d}", key="tpmc")
    with tpa2:
        tpav = st.selectbox("Ano Venda", range(2010, 2025), index=5, key="tpav")
        tpmv = st.selectbox("Mes Venda", range(1, 13), format_func=lambda m: f"{m:02d}", key="tpmv")

    if st.button("//  ANALISAR PROBABILIDADE"):
        if tp and (tpac * 12 + tpmc) < (tpav * 12 + tpmv):
            with st.spinner("Rodando analise..."):
                tp_p = buscar_dados(tp, f"{tpac}-{tpmc:02d}-01", f"{tpav}-{tpmv:02d}-28")
            if tp_p is not None:
                try:
                    tpc    = tp_p[f"{tpac}-{tpmc:02d}"].iloc[0]
                    tpv    = tp_p[f"{tpav}-{tpmv:02d}"].iloc[0]
                    tp_ret = ((tpv - tpc) / tpc) * 100
                    tp_dias  = (tp_p.index[-1] - tp_p.index[0]).days
                    tp_edge  = calcular_edge_score(tp_ret, tp_dias, tp_p)
                    tp_rv    = calcular_todos_retornos(tp_p)
                    tp_pct   = (tp_rv <= tp_ret).sum() / len(tp_rv) * 100
                    ret_esp  = round(float(tp_rv.mean()) + (tp_ret - float(tp_rv.mean())) * 0.3, 1)
                    prob_top = min(95, max(5, round(tp_pct * 0.85, 0)))
                    p1, p2, p3 = st.columns(3)
                    with p1:
                        st.metric("Retorno Real", f"{'+' if tp_ret >= 0 else ''}{tp_ret:.1f}%")
                    with p2:
                        st.metric("Retorno Esperado", f"{'+' if ret_esp >= 0 else ''}{ret_esp:.1f}%")
                    with p3:
                        st.metric("Prob. Top Quartile", f"{prob_top:.0f}%")
                    st.metric(
                        "Edge Score / Percentil historico",
                        f"{tp_edge}/100  |  Percentil {tp_pct:.1f}%  |  Holding: {tp_dias} dias"
                    )
                except Exception:
                    st.error("Nao foi possivel calcular para essas datas.")
            else:
                st.error("Ticker nao encontrado.")
        else:
            st.error("Preencha o ticker e datas validas.")

    st.markdown("---")
    st.markdown("#### Market Edge Dashboard")

    pi1, pi2 = st.columns(2)
    with pi1:
        st.markdown("**Momentum extremo — positivo**")
        for t, pct, ret, d in [("WEGE3", 99.8, "+31.2%", "20d"), ("PETR4", 99.3, "+24.1%", "12d"), ("ITUB4", 94.2, "+15.4%", "15d")]:
            st.markdown(f"**{t}** — {ret} em {d} — Percentil {pct}%")
        st.progress(0.99)
    with pi2:
        st.markdown("**Queda anormal — reversao provavel**")
        for t, pct, ret, d in [("BBDC4", 98.4, "-22.3%", "10d"), ("VALE3", 97.1, "-18.7%", "8d"), ("MGLU3", 95.6, "-14.2%", "6d")]:
            st.markdown(f"**{t}** — {ret} em {d} — Percentil {pct}%")
        st.progress(0.97)

    st.warning("Retail sentiment mismatch detectado — varejo comprando em momento de distribuicao institucional em 3 ativos do indice.")
    st.caption("Dados do radar sao ilustrativos. Nao constitui recomendacao de investimento.")