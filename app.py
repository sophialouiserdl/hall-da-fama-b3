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

LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="38" height="38" style="flex-shrink:0">'
    '<defs>'
    '<clipPath id="lc"><circle cx="98" cy="98" r="76"/></clipPath>'
    '<linearGradient id="lg" x1="0%" y1="0%" x2="0%" y2="100%">'
    '<stop offset="0%" stop-color="#C8F400" stop-opacity="0.25"/>'
    '<stop offset="100%" stop-color="#C8F400" stop-opacity="0"/>'
    '</linearGradient>'
    '</defs>'
    '<circle cx="98" cy="98" r="80" fill="none" stroke="#C8F400" stroke-width="5"/>'
    '<circle cx="98" cy="98" r="70" fill="none" stroke="#C8F400" stroke-width="1" opacity="0.2"/>'
    '<g clip-path="url(#lc)">'
    '<polygon points="22,152 46,144 62,150 78,130 92,122 104,108 116,112 130,88 146,80 164,58 176,52 176,185 22,185" fill="url(#lg)"/>'
    '<polyline points="22,152 46,144 62,150 78,130 92,122 104,108 116,112 130,88 146,80 164,58 176,52"'
    ' fill="none" stroke="#C8F400" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="176" cy="52" r="6" fill="#C8F400"/>'
    '<circle cx="176" cy="52" r="11" fill="none" stroke="#C8F400" stroke-width="1.5" opacity="0.4"/>'
    '</g>'
    '<line x1="162" y1="162" x2="202" y2="202" stroke="#C8F400" stroke-width="11" stroke-linecap="round"/>'
    '<line x1="162" y1="162" x2="202" y2="202" stroke="#0A0A0A" stroke-width="3.5" stroke-linecap="round"/>'
    '</svg>'
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
  --bg:       #0A0A0A;
  --surface:  #111111;
  --card:     #161616;
  --border:   rgba(200,244,0,0.18);
  --accent:   #C8F400;
  --accent2:  #00E87A;
  --danger:   #FF4040;
  --text:     #E8E4D8;
  --muted:    rgba(232,228,216,0.4);
  --mono:     'IBM Plex Mono', monospace;
  --display:  'Syne', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
}

.block-container {
    max-width: 1100px !important;
    padding: 100px 2rem 4rem 2rem !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

#MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }

/* ── FIXED HEADER ── */
.al-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: rgba(10,10,10,0.96);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 12px 40px;
    display: flex;
    align-items: center;
    gap: 18px;
}
.al-logo-text {
    font-family: var(--display);
    font-size: 26px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: 3px;
    line-height: 1;
}
.al-tagline {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    border-left: 1px solid var(--border);
    padding-left: 18px;
    margin-left: 4px;
}
.al-badge {
    margin-left: auto;
    background: var(--accent);
    color: #0A0A0A;
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 2px;
    padding: 4px 10px;
    text-transform: uppercase;
}

/* ── SECTION HEADERS ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 48px 0 24px 0;
}
.section-num {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--accent);
    letter-spacing: 2px;
    opacity: 0.6;
}
.section-title {
    font-family: var(--display);
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: 1px;
}
.section-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── CARDS ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent);
    opacity: 0.6;
}

.card-accent {
    background: var(--accent);
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}

/* ── INFO BUBBLES ── */
.bubble-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 20px 0;
}
.bubble {
    background: var(--card);
    border: 1px solid var(--border);
    padding: 20px 22px;
    position: relative;
    clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
}
.bubble::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 16px; height: 16px;
    background: var(--accent);
    clip-path: polygon(0 0, 100% 100%, 100% 0);
    opacity: 0.5;
}
.bubble-label {
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.bubble-value {
    font-family: var(--display);
    font-size: 32px;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}
.bubble-value.green { color: var(--accent2); }
.bubble-value.red   { color: var(--danger); }
.bubble-value.white { color: var(--text); }
.bubble-sub {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--muted);
    margin-top: 6px;
}

/* ── RANK CARD ── */
.rank-row {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
}
.rank-row:hover { background: rgba(200,244,0,0.04); }
.rank-pos {
    font-family: var(--display);
    font-size: 22px;
    font-weight: 800;
    color: var(--muted);
    width: 32px;
    text-align: center;
    flex-shrink: 0;
}
.rank-ticker {
    font-family: var(--display);
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    width: 72px;
    flex-shrink: 0;
}
.rank-label {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    flex: 1;
}
.rank-ret {
    font-family: var(--display);
    font-size: 20px;
    font-weight: 800;
    text-align: right;
    flex-shrink: 0;
}
.rank-bar-wrap {
    width: 100px;
    height: 3px;
    background: rgba(255,255,255,0.06);
    flex-shrink: 0;
}
.rank-bar-fill {
    height: 3px;
    border-radius: 2px;
}

/* ── VERDICT BOX ── */
.verdict {
    padding: 28px 32px;
    border: 1px solid;
    position: relative;
    margin: 20px 0;
    clip-path: polygon(0 0, calc(100% - 24px) 0, 100% 24px, 100% 100%, 24px 100%, 0 calc(100% - 24px));
}
.verdict-icon {
    font-size: 36px;
    margin-bottom: 10px;
    display: block;
}
.verdict-title {
    font-family: var(--display);
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.verdict-text {
    font-family: var(--mono);
    font-size: 13px;
    line-height: 1.7;
    opacity: 0.8;
}

/* ── EDGE SCORE ── */
.edge-ring {
    display: flex;
    align-items: center;
    gap: 28px;
    padding: 24px;
    background: var(--card);
    border: 1px solid var(--border);
}
.edge-score-num {
    font-family: var(--display);
    font-size: 72px;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}
.edge-score-label {
    font-family: var(--display);
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 2px;
}
.edge-bar-track {
    flex: 1;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 4px;
    overflow: hidden;
}
.edge-bar-fill {
    height: 8px;
    border-radius: 4px;
    background: var(--accent);
    transition: width 0.6s ease;
}

/* ── HALL ROWS ── */
.hall-header {
    background: var(--accent);
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2px;
}
.hall-header-text {
    font-family: var(--display);
    font-size: 14px;
    font-weight: 800;
    color: #0A0A0A;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── STAT DIAMOND ── */
.diamond-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.diamond-card {
    background: var(--card);
    border: 1px solid var(--border);
    padding: 18px 20px;
    position: relative;
}
.diamond-card::before {
    content: attr(data-icon);
    position: absolute;
    top: 12px;
    right: 14px;
    font-size: 18px;
    opacity: 0.25;
}
.diamond-card-label {
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.diamond-card-val {
    font-family: var(--display);
    font-size: 26px;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
}

/* ── INTELLIGENCE ── */
.radar-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: var(--card);
    border: 1px solid var(--border);
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.radar-row::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
}
.radar-row.up::before   { background: var(--accent2); }
.radar-row.down::before { background: var(--danger); }
.radar-ticker {
    font-family: var(--display);
    font-size: 18px;
    font-weight: 800;
    color: var(--text);
    width: 68px;
}
.radar-ret {
    font-family: var(--display);
    font-size: 18px;
    font-weight: 700;
    width: 80px;
}
.radar-ret.up   { color: var(--accent2); }
.radar-ret.down { color: var(--danger); }
.radar-signal {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    flex: 1;
    color: var(--muted);
}
.radar-pct {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent);
}

/* ── SHARE CARD ── */
.share-card {
    background: #0D0D0D;
    border: 1px solid var(--border);
    padding: 28px 32px;
    font-family: var(--mono);
    font-size: 13px;
    color: var(--text);
    line-height: 1.9;
    white-space: pre;
    overflow-x: auto;
}

/* ── INPUTS OVERRIDES ── */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stNumberInput"] > div > div > input {
    background: var(--card) !important;
    border: 1px solid rgba(200,244,0,0.3) !important;
    border-radius: 0 !important;
    font-family: var(--mono) !important;
    font-size: 15px !important;
    color: var(--text) !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stNumberInput"] > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,244,0,0.1) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    font-family: var(--mono) !important;
    font-size: 9px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-baseweb="select"] > div {
    background: var(--card) !important;
    border: 1px solid rgba(200,244,0,0.3) !important;
    border-radius: 0 !important;
    font-family: var(--mono) !important;
    color: var(--text) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,244,0,0.1) !important;
}
[data-baseweb="popover"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
}
li[role="option"] {
    font-family: var(--mono) !important;
    background: var(--card) !important;
    color: var(--text) !important;
}
li[role="option"]:hover { background: rgba(200,244,0,0.08) !important; }

/* ── BUTTON ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: var(--display) !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    letter-spacing: 3px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all 0.15s !important;
    text-transform: uppercase !important;
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px)) !important;
}
.stButton > button:hover {
    background: #d8ff00 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(200,244,0,0.25) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    padding: 16px 18px !important;
}
[data-testid="stMetricLabel"] > div { color: var(--muted) !important; font-family: var(--mono) !important; font-size: 9px !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: var(--display) !important; font-size: 30px !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-family: var(--mono) !important; font-size: 11px !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-width: 1px !important;
    border-style: solid !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 32px 0 !important;
}

/* ── PROGRESS ── */
.stProgress > div > div {
    background: rgba(200,244,0,0.1) !important;
    border-radius: 0 !important;
    height: 4px !important;
}
.stProgress > div > div > div > div {
    background: var(--accent) !important;
    border-radius: 0 !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── COLUMNS SPACING ── */
[data-testid="column"] { padding: 0 8px !important; }

/* ── PLOTLY WRAPPER ── */
.js-plotly-plot { border: 1px solid var(--border) !important; }

/* ── TABLE ── */
table { border-collapse: collapse !important; width: 100% !important; border: 1px solid var(--border) !important; }
th { background: var(--card) !important; color: var(--accent) !important; font-family: var(--display) !important; font-size: 12px !important; font-weight: 700 !important; letter-spacing: 2px !important; padding: 12px 16px !important; border: 1px solid var(--border) !important; text-align: left !important; }
td { padding: 10px 16px !important; border: 1px solid var(--border) !important; font-family: var(--mono) !important; font-size: 12px !important; background: var(--card) !important; color: var(--text) !important; }
tr:hover td { background: rgba(200,244,0,0.04) !important; }

/* ── STCAPTION ── */
.stCaption { font-family: var(--mono) !important; font-size: 10px !important; opacity: 0.3 !important; letter-spacing: 1px !important; }

/* ── INFO CALLOUT BOXES ── */
.callout {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 18px 20px;
    border: 1px solid var(--border);
    background: var(--card);
    margin: 12px 0;
}
.callout-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }
.callout-body { flex: 1; }
.callout-title { font-family: var(--display); font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.callout-text  { font-family: var(--mono); font-size: 12px; color: var(--muted); line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="al-header">'
    + LOGO_SVG +
    '<div class="al-logo-text">ALPHALENS</div>'
    '<div class="al-tagline">Hall da Fama B3 &middot; Analise Quantitativa de Trades</div>'
    '<div class="al-badge">B3 &nbsp;·&nbsp; Brasil</div>'
    '</div>',
    unsafe_allow_html=True
)


def buscar_dados(ticker, start, end):
    d = yf.download(f"{ticker}.SA", start=start, end=end, auto_adjust=True, progress=False)
    if d.empty:
        return None
    return pd.Series(d["Close"].values.flatten(), index=d.index)


def calcular_todos_retornos(preco):
    p = preco.values
    n = len(p)
    m = (p[np.newaxis, :] - p[:, np.newaxis]) / p[:, np.newaxis]
    mask = np.triu(np.ones((n, n), dtype=bool), k=1)
    return m[mask] * 100


def calcular_edge_score(retorno, dias, serie):
    sr = min(40, max(0, (retorno / 200) * 40)) if retorno > 0 else max(-20, (retorno / 100) * 20)
    se = min(25, max(0, (retorno / max(1, dias)) * 30))
    vol = serie.pct_change().dropna().std() * np.sqrt(252) * 100
    sv = max(0, 20 - (vol / 5))
    dd = ((serie - serie.cummax()) / serie.cummax() * 100).min()
    sd = max(0, 15 + (dd / 5))
    return min(100, max(0, round(sr + se + sv + sd)))


def classificar_edge(s):
    if s >= 85:   return "LENDARIO",    "▲▲▲", "#C8F400"
    elif s >= 70: return "EXCEPCIONAL", "▲▲",  "#00E87A"
    elif s >= 55: return "BOM",         "▲",   "#4aade0"
    elif s >= 40: return "MEDIANO",     "◆",   "#FF9800"
    else:         return "FRACO",       "▼",   "#FF4040"


def cdi_estimado(ac, mc, av, mv):
    anos = (av * 12 + mv - ac * 12 - mc) / 12
    return round((pow(1.105, anos) - 1) * 100, 1)


HALL_FAMA = [
    {"pos": 1, "ticker": "WEGE3", "ret": 8700, "label": "Jan 2010 → Jan 2024", "pct": 100},
    {"pos": 2, "ticker": "PRIO3", "ret": 1240, "label": "Mar 2020 → Ago 2022", "pct": 95},
    {"pos": 3, "ticker": "CPLE6", "ret": 890,  "label": "Abr 2020 → Dez 2021", "pct": 88},
    {"pos": 4, "ticker": "RADL3", "ret": 620,  "label": "Jan 2015 → Dez 2020", "pct": 80},
    {"pos": 5, "ticker": "RENT3", "ret": 480,  "label": "Jan 2018 → Jan 2022", "pct": 70},
    {"pos": 6, "ticker": "VALE3", "ret": 340,  "label": "Mar 2020 → Jul 2021", "pct": 60},
    {"pos": 7, "ticker": "PETR4", "ret": 310,  "label": "Jan 2016 → Jun 2022", "pct": 55},
    {"pos": 8, "ticker": "ITUB4", "ret": 156,  "label": "Jan 2016 → Jan 2020", "pct": 40},
]

HALL_VERGONHA = [
    {"pos": 1, "ticker": "OIBR3", "ret": -99, "label": "Jan 2014 → Dez 2023", "pct": 100},
    {"pos": 2, "ticker": "MGLU3", "ret": -92, "label": "Nov 2021 → Jan 2023", "pct": 92},
    {"pos": 3, "ticker": "VVAR3", "ret": -88, "label": "Ago 2021 → Jun 2023", "pct": 88},
    {"pos": 4, "ticker": "CESP3", "ret": -71, "label": "Jan 2010 → Dez 2015", "pct": 71},
    {"pos": 5, "ticker": "BVMF3", "ret": -58, "label": "Mai 2019 → Mar 2020", "pct": 58},
]

RADAR = [
    {"ticker": "PETR4", "ret": 24.1,  "dias": 12, "pct": 99.3, "signal": "MOMENTUM EXTREMO",  "dir": "up"},
    {"ticker": "VALE3", "ret": -18.7, "dias": 8,  "pct": 97.1, "signal": "REVERSAO PROVAVEL", "dir": "down"},
    {"ticker": "WEGE3", "ret": 31.2,  "dias": 20, "pct": 99.8, "signal": "RARO HISTORICO",    "dir": "up"},
    {"ticker": "ITUB4", "ret": 15.4,  "dias": 15, "pct": 94.2, "signal": "ACIMA DA MEDIA",    "dir": "up"},
    {"ticker": "BBDC4", "ret": -22.3, "dias": 10, "pct": 98.4, "signal": "QUEDA ANORMAL",     "dir": "down"},
]

PLOTLY_THEME = dict(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#0A0A0A",
    font=dict(color="#E8E4D8", family="IBM Plex Mono"),
    margin=dict(l=16, r=16, t=40, b=16),
    xaxis=dict(gridcolor="rgba(200,244,0,0.05)", linecolor="rgba(200,244,0,0.15)", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="rgba(200,244,0,0.05)", linecolor="rgba(200,244,0,0.15)", tickfont=dict(size=10)),
)


st.markdown("""
<div class="section-label">
  <span class="section-num">01</span>
  <span class="section-title">Analisar Trade</span>
  <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <div class="callout-icon">◎</div>
  <div class="callout-body">
    <div class="callout-title">Como funciona</div>
    <div class="callout-text">Insira o ticker, o periodo do seu trade e o valor investido. O AlphaLens vai calcular quantos % voce ganhou, ranquear sua operacao entre <strong>todos os trades possiveis</strong> naquele ativo no periodo, e te dizer onde voce ficou na historia da B3.</div>
  </div>
</div>
""", unsafe_allow_html=True)

col_form1, col_form2, col_form3 = st.columns([2, 1, 1])
with col_form1:
    ticker = st.text_input("Ticker", placeholder="Ex: PETR4, WEGE3, VALE3").upper().strip()

with col_form2:
    ano_compra = st.selectbox("Ano de Compra", range(2010, 2026))
with col_form3:
    mes_compra = st.selectbox("Mes de Compra", range(1, 13), format_func=lambda m: f"{m:02d}")

col_form4, col_form5, col_form6 = st.columns([2, 1, 1])
with col_form4:
    investido = st.number_input("Valor Investido R$ (opcional)", min_value=0.0, value=0.0, step=500.0)
with col_form5:
    ano_venda = st.selectbox("Ano de Venda", range(2010, 2026), index=10)
with col_form6:
    mes_venda = st.selectbox("Mes de Venda", range(1, 13), format_func=lambda m: f"{m:02d}")

analisar = st.button("▲  ANALISAR MEU TRADE")

if analisar:
    if not ticker:
        st.error("Digite um ticker para continuar.")
    elif (ano_compra, mes_compra) >= (ano_venda, mes_venda):
        st.error("A data de compra precisa ser anterior a data de venda.")
    else:
        with st.spinner("Buscando dados na B3..."):
            dados = yf.download(
                f"{ticker}.SA",
                start=f"{ano_compra}-{mes_compra:02d}-01",
                end=f"{ano_venda}-{mes_venda:02d}-28",
                auto_adjust=True, progress=False
            )
        if dados.empty:
            st.error(f"Ticker '{ticker}' nao encontrado. Verifique se o codigo esta correto.")
        else:
            preco = pd.Series(dados["Close"].values.flatten(), index=dados.index)
            try:
                preco_compra = float(preco[f"{ano_compra}-{mes_compra:02d}"].iloc[0])
                preco_venda  = float(preco[f"{ano_venda}-{mes_venda:02d}"].iloc[0])
            except (KeyError, IndexError):
                st.error("Nao foi possivel encontrar precos para as datas selecionadas.")
                st.stop()

            retorno = ((preco_venda - preco_compra) / preco_compra) * 100
            p_arr = preco.values
            n = len(p_arr)
            mat = (p_arr[np.newaxis, :] - p_arr[:, np.newaxis]) / p_arr[:, np.newaxis]
            mask = np.triu(np.ones((n, n), dtype=bool), k=1)
            rv = mat[mask] * 100
            total     = len(rv)
            melhor    = float(rv.max())
            pior      = float(rv.min())
            posicao   = int((rv <= retorno).sum())
            percentil = (posicao / total) * 100
            top_pct   = 100 - percentil
            rank_num  = total - posicao + 1
            dias_h    = (preco.index[-1] - preco.index[0]).days
            edge      = calcular_edge_score(retorno, dias_h, preco)
            elabel, eicon, ecor = classificar_edge(edge)
            cdi = cdi_estimado(ano_compra, mes_compra, ano_venda, mes_venda)
            vs_cdi = round(retorno - cdi, 1)

            st.session_state["resultado"] = dict(
                ticker=ticker, preco=preco,
                retorno=retorno, edge=edge, elabel=elabel, eicon=eicon, ecor=ecor,
                rank_num=rank_num, total=total, top_pct=top_pct, percentil=percentil,
                melhor=melhor, pior=pior,
                preco_compra=preco_compra, preco_venda=preco_venda,
                dias_h=dias_h, cdi=cdi, vs_cdi=vs_cdi,
                ano_c=ano_compra, mes_c=mes_compra,
                ano_v=ano_venda, mes_v=mes_venda,
                investido=investido, rv=rv
            )

if "resultado" in st.session_state:
    r = st.session_state["resultado"]
    ret = r["retorno"]
    ret_cor = "green" if ret >= 0 else "red"

    st.markdown("""
    <div class="section-label" style="margin-top:36px">
      <span class="section-num">→</span>
      <span class="section-title">Resultado</span>
      <span class="section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    ret_sinal = "+" if ret >= 0 else ""
    st.markdown(f"""
    <div class="bubble-grid">
      <div class="bubble">
        <div class="bubble-label">Retorno do Trade</div>
        <div class="bubble-value {ret_cor}">{ret_sinal}{ret:.1f}%</div>
        <div class="bubble-sub">R$ {r['preco_compra']:.2f} &rarr; R$ {r['preco_venda']:.2f}</div>
      </div>
      <div class="bubble">
        <div class="bubble-label">Posicao no Ranking</div>
        <div class="bubble-value white">#{r['rank_num']:,}</div>
        <div class="bubble-sub">de {r['total']:,} trades possiveis</div>
      </div>
      <div class="bubble">
        <div class="bubble-label">Percentil Historico</div>
        <div class="bubble-value {'green' if r['top_pct'] <= 30 else ('red' if r['top_pct'] >= 70 else 'white')}">Top {r['top_pct']:.1f}%</div>
        <div class="bubble-sub">melhor que {r['percentil']:.1f}% dos trades</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if r["investido"] > 0:
        reais_end  = round(r["investido"] * (1 + ret / 100))
        reais_best = round(r["investido"] * (1 + r["melhor"] / 100))
        delta_r = reais_end - r["investido"]
        delta_sinal = "+" if delta_r >= 0 else ""
        st.markdown(f"""
        <div class="bubble-grid" style="grid-template-columns:repeat(2,1fr)">
          <div class="bubble">
            <div class="bubble-label">Seu investimento virou</div>
            <div class="bubble-value {'green' if delta_r>=0 else 'red'}">R$ {reais_end:,.0f}</div>
            <div class="bubble-sub">{delta_sinal}R$ {abs(delta_r):,.0f} ({ret_sinal}{ret:.1f}%)</div>
          </div>
          <div class="bubble">
            <div class="bubble-label">No melhor trade possivel</div>
            <div class="bubble-value white">R$ {reais_best:,.0f}</div>
            <div class="bubble-sub">+R$ {reais_best - reais_end:,.0f} a mais</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    edge_pct = r["edge"]
    st.markdown(f"""
    <div class="edge-ring">
      <div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:rgba(232,228,216,0.4);text-transform:uppercase;margin-bottom:4px">Edge Score</div>
        <div class="edge-score-num" style="color:{r['ecor']}">{edge_pct}</div>
        <div style="color:{r['ecor']};font-family:'Syne',sans-serif;font-size:13px;font-weight:700;letter-spacing:2px;margin-top:4px">{r['eicon']} {r['elabel']}</div>
      </div>
      <div style="flex:1">
        <div style="display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;font-size:9px;color:rgba(232,228,216,0.35);letter-spacing:2px;margin-bottom:6px">
          <span>FRACO</span><span>MEDIANO</span><span>BOM</span><span>EXCEPCIONAL</span><span>LENDARIO</span>
        </div>
        <div class="edge-bar-track">
          <div class="edge-bar-fill" style="width:{edge_pct}%;background:{r['ecor']}"></div>
        </div>
        <div style="margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:8px">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.45)">
            vs CDI: <span style="color:{'#00E87A' if r['vs_cdi']>=0 else '#FF4040'};font-weight:500">{'+'if r['vs_cdi']>=0 else ''}{r['vs_cdi']:.1f} p.p.</span>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.45)">
            Holding: <span style="color:#E8E4D8">{r['dias_h']} dias</span>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.45)">
            Melhor possivel: <span style="color:#00E87A">+{r['melhor']:.1f}%</span>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.45)">
            CDI estimado: <span style="color:#E8E4D8">+{r['cdi']}%</span>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if r["top_pct"] <= 10:
        v_bg, v_border, v_col = "#0a1a00", "#00E87A", "#00E87A"
        v_icon, v_titulo = "◎", f"TOP {r['top_pct']:.1f}% — TRADE HISTORICO"
        v_texto = f"De {r['total']:,} combinacoes possiveis com {r['ticker']}, o seu ficou entre os melhores ja alcancaveis. Voce superou {r['percentil']:.1f}% de todas as operacoes possiveis."
    elif r["top_pct"] <= 30:
        v_bg, v_border, v_col = "#0a1a00", "#C8F400", "#C8F400"
        v_icon, v_titulo = "▲▲", f"TOP {r['top_pct']:.1f}% — EXCEPCIONAL"
        v_texto = f"Voce superou {r['percentil']:.1f}% de todos os trades possiveis com {r['ticker']}. Poucos conseguem estar nesse quartil."
    elif r["top_pct"] <= 50:
        v_bg, v_border, v_col = "#0a0a1a", "#4aade0", "#4aade0"
        v_icon, v_titulo = "▲", f"TOP {r['top_pct']:.1f}% — ACIMA DA MEDIA"
        v_texto = f"Voce superou mais da metade das possibilidades. O melhor trade com {r['ticker']} no periodo teria chegado a +{r['melhor']:.1f}%."
    elif r["top_pct"] <= 75:
        v_bg, v_border, v_col = "#1a0f00", "#FF9800", "#FF9800"
        v_icon, v_titulo = "◆", f"BOTTOM {100-r['top_pct']:.0f}% — ABAIXO DA MEDIA"
        v_texto = f"O timing nao foi o melhor. O mesmo ativo nas datas ideais teria chegado a +{r['melhor']:.1f}%. Voce ficou na metade inferior."
    else:
        v_bg, v_border, v_col = "#1a0000", "#FF4040", "#FF4040"
        v_icon, v_titulo = "▼", f"BOTTOM {100-r['top_pct']:.0f}% — TIMING CATASTROFICO"
        v_texto = f"Entre os {100-r['top_pct']:.0f}% piores trades possiveis. O mesmo ativo nas datas certas teria rendido +{r['melhor']:.1f}%."

    st.markdown(f"""
    <div class="verdict" style="background:{v_bg};border-color:{v_border};margin-top:20px">
      <span class="verdict-icon" style="color:{v_col}">{v_icon}</span>
      <div class="verdict-title" style="color:{v_col}">{v_titulo}</div>
      <div class="verdict-text">{v_texto}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label" style="margin-top:36px">
      <span class="section-num">→</span>
      <span class="section-title">Distribuicao de Trades Possiveis</span>
      <span class="section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    df_hist = pd.DataFrame({"retorno": r["rv"]})
    fig = px.histogram(df_hist, x="retorno", nbins=80, color_discrete_sequence=["rgba(200,244,0,0.35)"])
    fig.add_vline(
        x=r["retorno"], line_color="#C8F400", line_width=2,
        annotation_text="VOCE", annotation_font_color="#C8F400", annotation_font_size=11
    )
    fig.update_traces(marker_line_color="rgba(200,244,0,0.6)", marker_line_width=0.3)
    fig.update_layout(**PLOTLY_THEME, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="section-label" style="margin-top:36px">
      <span class="section-num">→</span>
      <span class="section-title">Trade Replay</span>
      <span class="section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    preco_s = r["preco"]
    base = float(preco_s.iloc[0])
    acum = ((preco_s - base) / base * 100)

    marcos_idx  = [0, len(preco_s)//4, len(preco_s)//2, 3*len(preco_s)//4, len(preco_s)-1]
    marcos_nome = ["Compra", "25%", "Metade", "75%", "Venda"]
    cols_m = st.columns(5)
    for i, (idx, nome) in enumerate(zip(marcos_idx, marcos_nome)):
        with cols_m[i]:
            val  = float(acum.iloc[idx])
            data = preco_s.index[idx].strftime("%d/%m/%y")
            cor  = "#00E87A" if val >= 0 else "#FF4040"
            st.markdown(f"""
            <div style="background:#161616;border:1px solid rgba(200,244,0,0.12);padding:14px 16px;text-align:center">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:rgba(232,228,216,0.35);text-transform:uppercase;margin-bottom:6px">{nome}</div>
              <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:{cor}">{'+' if val>=0 else ''}{val:.1f}%</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,216,0.3);margin-top:4px">{data}</div>
            </div>
            """, unsafe_allow_html=True)

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(
        x=acum.index, y=acum.values,
        fill="tozeroy", fillcolor="rgba(200,244,0,0.05)",
        line=dict(color="#C8F400", width=2.5),
        hovertemplate="%{x|%d/%m/%Y}<br>Retorno: %{y:.2f}%<extra></extra>"
    ))
    fig_r.add_hline(y=0, line_color="rgba(255,255,255,0.1)", line_dash="dash")
    fig_r.add_trace(go.Scatter(
        x=[acum.index[0]], y=[0], mode="markers+text",
        marker=dict(size=10, color="#C8F400", symbol="circle"),
        text=["COMPRA"], textposition="top right", textfont=dict(color="#C8F400", size=10), showlegend=False
    ))
    ret_f = float(acum.iloc[-1])
    fig_r.add_trace(go.Scatter(
        x=[acum.index[-1]], y=[ret_f], mode="markers+text",
        marker=dict(size=10, color="#FF4040"),
        text=[f"VENDA {'+' if ret_f>=0 else ''}{ret_f:.1f}%"],
        textposition="top left", textfont=dict(color="#FF4040", size=10), showlegend=False
    ))
    fig_r.add_trace(go.Scatter(
        x=[acum.idxmax()], y=[float(acum.max())], mode="markers+text",
        marker=dict(size=9, color="#00E87A", symbol="triangle-up"),
        text=[f"MAX +{acum.max():.1f}%"], textposition="top center",
        textfont=dict(color="#00E87A", size=10), showlegend=False
    ))
    fig_r.add_trace(go.Scatter(
        x=[acum.idxmin()], y=[float(acum.min())], mode="markers+text",
        marker=dict(size=9, color="#FF9800", symbol="triangle-down"),
        text=[f"MIN {acum.min():.1f}%"], textposition="bottom center",
        textfont=dict(color="#FF9800", size=10), showlegend=False
    ))
    fig_r.update_layout(**PLOTLY_THEME, height=380, showlegend=False,
                        yaxis=dict(gridcolor="rgba(200,244,0,0.05)", ticksuffix="%"))
    st.plotly_chart(fig_r, use_container_width=True)

    if float(acum.min()) < -15:
        st.markdown(f"""<div class="callout"><div class="callout-icon">⚠</div><div class="callout-body"><div class="callout-title">Stop Emocional</div><div class="callout-text">Durante o trade voce chegou a estar <strong>{acum.min():.1f}%</strong> no negativo. Estudos mostram que a maioria dos traders de varejo venderia nesse ponto por stop emocional — perdendo a recuperacao.</div></div></div>""", unsafe_allow_html=True)
    if float(acum.max()) > ret_f + 10:
        st.markdown(f"""<div class="callout"><div class="callout-icon">◎</div><div class="callout-body"><div class="callout-title">Saida antes do Fim</div><div class="callout-text">O pico do trade foi <strong>+{acum.max():.1f}%</strong>. Voce encerrou quando ja havia recuado <strong>{acum.max()-ret_f:.1f} pontos percentuais</strong> do topo.</div></div></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label" style="margin-top:36px">
      <span class="section-num">→</span>
      <span class="section-title">E se voce tivesse segurado?</span>
      <span class="section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Buscando dados pos-venda..."):
        preco_pos = buscar_dados(
            r["ticker"],
            f"{r['ano_v']}-{r['mes_v']:02d}-01",
            str(datetime.today().date())
        )

    if preco_pos is not None and len(preco_pos) > 30:
        pv = float(r["preco_venda"])
        pc = float(r["preco_compra"])
        preco_hoje  = float(preco_pos.iloc[-1])
        ret_pos = ((preco_hoje - pv) / pv) * 100
        ret_tot = ((preco_hoje - pc) / pc) * 100
        rp_cor  = "green" if ret_pos >= 0 else "red"
        rt_cor  = "green" if ret_tot >= 0 else "red"
        st.markdown(f"""
        <div class="bubble-grid">
          <div class="bubble">
            <div class="bubble-label">Voce vendeu em</div>
            <div class="bubble-value {ret_cor}">{'+' if ret>=0 else ''}{ret:.1f}%</div>
            <div class="bubble-sub">{r['mes_v']:02d}/{r['ano_v']}</div>
          </div>
          <div class="bubble">
            <div class="bubble-label">Apos sua venda o ativo foi</div>
            <div class="bubble-value {rp_cor}">{'+' if ret_pos>=0 else ''}{ret_pos:.1f}%</div>
            <div class="bubble-sub">ate hoje</div>
          </div>
          <div class="bubble">
            <div class="bubble-label">Se tivesse segurado</div>
            <div class="bubble-value {rt_cor}">{'+' if ret_tot>=0 else ''}{ret_tot:.1f}%</div>
            <div class="bubble-sub">retorno total acumulado</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=preco_s.index, y=preco_s.values,
            name="Seu periodo", line=dict(color="#C8F400", width=2.5)
        ))
        fig2.add_trace(go.Scatter(
            x=preco_pos.index, y=preco_pos.values,
            name="Apos saida", line=dict(color="#FF4040", width=2, dash="dot")
        ))
        data_saida = preco_pos.index[0]
        fig2.add_shape(type="line", x0=data_saida, x1=data_saida, y0=0, y1=1,
                       xref="x", yref="paper", line=dict(color="rgba(255,255,255,0.2)", dash="dot"))
        fig2.add_annotation(x=data_saida, y=1, xref="x", yref="paper",
                            text="VOCE SAIU", showarrow=False,
                            font=dict(color="rgba(232,228,216,0.5)", size=10), yanchor="bottom")
        fig2.update_layout(**PLOTLY_THEME, height=340, legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True)

        if ret_pos > 20:
            st.markdown(f"""<div class="callout"><div class="callout-icon">◈</div><div class="callout-body"><div class="callout-title">Saida Cedo Demais</div><div class="callout-text">O ativo subiu mais <strong>{ret_pos:.1f}%</strong> depois que voce saiu. Se tivesse mantido, seu retorno total seria <strong>{ret_tot:.1f}%</strong>.</div></div></div>""", unsafe_allow_html=True)
        elif ret_pos < -10:
            st.markdown(f"""<div class="callout"><div class="callout-icon">◎</div><div class="callout-body"><div class="callout-title">Timing de Saida Correto</div><div class="callout-text">O ativo caiu <strong>{abs(ret_pos):.1f}%</strong> depois que voce vendeu. Voce saiu na hora certa.</div></div></div>""", unsafe_allow_html=True)

    reais_str = f"\nR${r['investido']:,.0f}  ->  R${round(r['investido']*(1+ret/100)):,.0f}" if r["investido"] > 0 else ""
    vs_cdi_str = f"{'+' if r['vs_cdi']>=0 else ''}{r['vs_cdi']:.1f} p.p."
    card_txt = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALPHALENS — MEU TRADE — B3{reais_str}

  Ticker    {r['ticker']}
  Periodo   {r['mes_c']:02d}/{r['ano_c']} -> {r['mes_v']:02d}/{r['ano_v']}
  Retorno   {'+' if ret>=0 else ''}{ret:.1f}%

  Edge Score   {r['edge']}/100  {r['eicon']} {r['elabel']}
  Ranking      #{r['rank_num']:,} de {r['total']:,} trades
  Percentil    Top {r['top_pct']:.1f}% historico
  vs CDI       {vs_cdi_str}

  hall-da-fama-b3.streamlit.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    st.markdown("""
    <div class="section-label" style="margin-top:36px">
      <span class="section-num">→</span>
      <span class="section-title">Card para Compartilhar</span>
      <span class="section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="share-card">{card_txt}</div>', unsafe_allow_html=True)
    st.caption("Copie o texto acima e cole no LinkedIn ou Twitter")


st.markdown("""
<div class="section-label" style="margin-top:56px">
  <span class="section-num">02</span>
  <span class="section-title">Hall da Fama B3</span>
  <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <div class="callout-icon">★</div>
  <div class="callout-body">
    <div class="callout-title">Os Imortais da Bolsa Brasileira</div>
    <div class="callout-text">Os maiores trades possiveis da historia da B3 — operacoes lendarias que definiram geracoes de investidores. Onde o seu trade se encaixa nessa historia?</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hall-header"><span class="hall-header-text">▲ Hall da Fama — Imortais</span></div>', unsafe_allow_html=True)
for item in HALL_FAMA:
    bar_w = int(item["pct"])
    st.markdown(f"""
    <div class="rank-row">
      <div class="rank-pos">#{item['pos']}</div>
      <div class="rank-ticker">{item['ticker']}</div>
      <div class="rank-label">{item['label']}</div>
      <div class="rank-bar-wrap"><div class="rank-bar-fill" style="width:{bar_w}%;background:#C8F400"></div></div>
      <div class="rank-ret" style="color:#C8F400">+{item['ret']:,}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="hall-header" style="background:#FF4040"><span class="hall-header-text" style="color:#0A0A0A">▼ Hall da Vergonha — Os Micos Eternos</span></div>', unsafe_allow_html=True)
for item in HALL_VERGONHA:
    bar_w = int(item["pct"])
    st.markdown(f"""
    <div class="rank-row">
      <div class="rank-pos" style="color:rgba(255,64,64,0.5)">#{item['pos']}</div>
      <div class="rank-ticker">{item['ticker']}</div>
      <div class="rank-label">{item['label']}</div>
      <div class="rank-bar-wrap"><div class="rank-bar-fill" style="width:{bar_w}%;background:#FF4040"></div></div>
      <div class="rank-ret" style="color:#FF4040">{item['ret']}%</div>
    </div>
    """, unsafe_allow_html=True)

if "resultado" in st.session_state:
    r = st.session_state["resultado"]
    ret = r["retorno"]
    ret_cor_hex = "#00E87A" if ret >= 0 else "#FF4040"
    st.markdown(f"""
    <div class="rank-row" style="background:rgba(200,244,0,0.06);border:1px solid rgba(200,244,0,0.25);margin-top:8px">
      <div class="rank-pos" style="color:#C8F400">✦</div>
      <div class="rank-ticker" style="color:#C8F400">{r['ticker']}</div>
      <div class="rank-label">{r['mes_c']:02d}/{r['ano_c']} → {r['mes_v']:02d}/{r['ano_v']}  ·  <strong>Seu trade</strong></div>
      <div class="rank-bar-wrap"><div class="rank-bar-fill" style="width:{min(100,max(2,abs(r['top_pct']))):.0f}%;background:{ret_cor_hex}"></div></div>
      <div class="rank-ret" style="color:{ret_cor_hex}">{'+' if ret>=0 else ''}{ret:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="section-label" style="margin-top:56px">
  <span class="section-num">03</span>
  <span class="section-title">Edge Score — Como e Calculado</span>
  <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <div class="callout-icon">◆</div>
  <div class="callout-body">
    <div class="callout-title">A metrica unica do AlphaLens</div>
    <div class="callout-text">Retorno bruto nao e tudo. Um trade de +50% em 1 semana e radicalmente diferente de +50% em 5 anos. O Edge Score combina 4 dimensoes para dar uma nota real a qualidade do seu timing.</div>
  </div>
</div>
""", unsafe_allow_html=True)

e1, e2 = st.columns(2)
with e1:
    st.markdown("""
    <div style="background:#161616;border:1px solid rgba(200,244,0,0.12);padding:24px 28px">
      <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:#C8F400;letter-spacing:2px;margin-bottom:20px;text-transform:uppercase">Composicao da Nota</div>
      <div style="display:flex;flex-direction:column;gap:14px">
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(200,244,0,0.08)">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8">Retorno %</span>
          <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#C8F400">40 pts</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(200,244,0,0.08)">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8">Eficiencia Temporal</span>
          <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#C8F400">25 pts</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(200,244,0,0.08)">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8">Volatilidade</span>
          <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#C8F400">20 pts</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8">Drawdown Maximo</span>
          <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#C8F400">15 pts</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with e2:
    tiers = [
        (85, 100, "LENDARIO",    "▲▲▲", "#C8F400"),
        (70, 84,  "EXCEPCIONAL", "▲▲",  "#00E87A"),
        (55, 69,  "BOM",         "▲",   "#4aade0"),
        (40, 54,  "MEDIANO",     "◆",   "#FF9800"),
        (0,  39,  "FRACO",       "▼",   "#FF4040"),
    ]
    tiers_html = ""
    for lo, hi, label, icon, cor in tiers:
        tiers_html += f"""
        <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid rgba(200,244,0,0.08)">
          <div style="font-family:'Syne',sans-serif;font-size:16px;color:{cor};width:28px">{icon}</div>
          <div style="flex:1;font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:{cor}">{label}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.35)">{lo}–{hi}</div>
        </div>"""
    st.markdown(f"""
    <div style="background:#161616;border:1px solid rgba(200,244,0,0.12);padding:24px 28px">
      <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:#C8F400;letter-spacing:2px;margin-bottom:20px;text-transform:uppercase">Classificacoes</div>
      {tiers_html}
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="section-label" style="margin-top:56px">
  <span class="section-num">04</span>
  <span class="section-title">Intelligence Engine</span>
  <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <div class="callout-icon">◈</div>
  <div class="callout-body">
    <div class="callout-title">Radar Institucional da B3</div>
    <div class="callout-text">Ativos com movimentos no percentil extremo do historico — metodologia quantitativa usada por fundos para detectar anomalias de mercado antes que virem consenso.</div>
  </div>
</div>
""", unsafe_allow_html=True)

for a in RADAR:
    ret_str  = f"{'+' if a['ret']>0 else ''}{a['ret']}%"
    ret_cor  = "up" if a["ret"] > 0 else "down"
    st.markdown(f"""
    <div class="radar-row {ret_cor}">
      <div class="radar-ticker">{a['ticker']}</div>
      <div class="radar-ret {ret_cor}">{ret_str}</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,216,0.35);width:60px">{a['dias']}d</div>
      <div class="radar-signal">{a['signal']}</div>
      <div style="width:100px">
        <div style="height:3px;background:rgba(255,255,255,0.06)">
          <div style="height:3px;width:{a['pct']}%;background:{'#00E87A' if a['ret']>0 else '#FF4040'}"></div>
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:rgba(232,228,216,0.3);margin-top:3px;text-align:right">P{a['pct']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    st.markdown("""
    <div style="background:#161616;border:1px solid rgba(200,244,0,0.12);padding:24px 28px;position:relative;overflow:hidden">
      <div style="position:absolute;top:-20px;right:-20px;font-size:100px;opacity:0.03;font-family:'Syne',sans-serif;font-weight:900">70</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:rgba(232,228,216,0.35);text-transform:uppercase;margin-bottom:12px">Varejo vende cedo demais</div>
      <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;color:#C8F400;line-height:1">70%</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8;margin:8px 0">dos trades top-30% encerrados antes do pico</div>
      <div style="height:4px;background:rgba(200,244,0,0.1);margin:14px 0"><div style="height:4px;width:70%;background:#C8F400;border-radius:2px"></div></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,216,0.35)">Retorno medio deixado na mesa: +34%</div>
    </div>
    """, unsafe_allow_html=True)
with b2:
    st.markdown("""
    <div style="background:#161616;border:1px solid rgba(200,244,0,0.12);padding:24px 28px;position:relative;overflow:hidden">
      <div style="position:absolute;top:-20px;right:-20px;font-size:100px;opacity:0.03;font-family:'Syne',sans-serif;font-weight:900">62</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:rgba(232,228,216,0.35);text-transform:uppercase;margin-bottom:12px">Varejo segura tarde demais</div>
      <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;color:#FF4040;line-height:1">62%</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#E8E4D8;margin:8px 0">dos trades negativos poderiam ter saido positivos</div>
      <div style="height:4px;background:rgba(255,64,64,0.1);margin:14px 0"><div style="height:4px;width:62%;background:#FF4040;border-radius:2px"></div></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,216,0.35)">Loss medio evitavel: -28%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:#161616;border:1px solid rgba(255,152,0,0.25);padding:18px 22px;margin-top:12px;display:flex;gap:14px;align-items:flex-start">
  <div style="font-size:18px;color:#FF9800;flex-shrink:0;margin-top:2px">◈</div>
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#FF9800;margin-bottom:4px">Retail Sentiment Mismatch</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(232,228,216,0.5);line-height:1.6">Varejo comprando em momento de distribuicao institucional detectado em 3 ativos do indice. Dados do radar sao ilustrativos. Nao constitui recomendacao de investimento.</div>
  </div>
</div>
<br><br>
""", unsafe_allow_html=True)