import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Hall da Fama & Vergonha: B3")
st.write("Rankeie seu trade na história da bolsa brasileira.")

ticker = st.text_input("Ticker", placeholder="Ex: PETR4").upper()

col1, col2 = st.columns(2)

with col1:
    ano_compra = st.selectbox("Ano de Compra", range(2010, 2025))
    mes_compra = st.selectbox("Mês de Compra", range(1, 13), format_func=lambda m: f"{m:02d}")

with col2:
    ano_venda = st.selectbox("Ano de Venda", range(2010, 2025), index=10)
    mes_venda = st.selectbox("Mês de Venda", range(1, 13), format_func=lambda m: f"{m:02d}")

if st.button("Analisar"):
    if not ticker:
        st.error("Digite um ticker!")
    elif (ano_compra, mes_compra) >= (ano_venda, mes_venda):
        st.error("A data de compra precisa ser antes da data de venda!")
    else:
        with st.spinner("Buscando dados..."):
            dados = yf.download(
                f"{ticker}.SA",
                start=f"{ano_compra}-{mes_compra:02d}-01",
                end=f"{ano_venda}-{mes_venda:02d}-28",
                auto_adjust=True,
                progress=False
            )

        if dados.empty:
            st.error(f"Ticker '{ticker}' não encontrado. Verifique se está correto.")
        else:
            preco = pd.Series(
                dados["Close"].values.flatten(),
                index=dados.index
            )

            st.success(f"✓ {len(preco)} dias de dados encontrados para {ticker}!")
            st.line_chart(preco)

            preco_compra = preco[f"{ano_compra}-{mes_compra:02d}"].iloc[0]
            preco_venda = preco[f"{ano_venda}-{mes_venda:02d}"].iloc[0]
            retorno = ((preco_venda - preco_compra) / preco_compra) * 100

            st.subheader("→ Seu Trade")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Preço de Compra", f"R$ {preco_compra:.2f}")
            with col_b:
                st.metric("Preço de Venda", f"R$ {preco_venda:.2f}")
            with col_c:
                st.metric("Retorno", f"{retorno:.1f}%")

            precos = preco.values
            n = len(precos)
            retornos_todos = (precos[np.newaxis, :] - precos[:, np.newaxis]) / precos[:, np.newaxis]
            mask = np.triu(np.ones((n, n), dtype=bool), k=1)
            retornos_validos = retornos_todos[mask] * 100

            total = len(retornos_validos)
            melhor = retornos_validos.max()
            pior = retornos_validos.min()
            posicao = (retornos_validos <= retorno).sum()
            percentil = (posicao / total) * 100

            st.subheader("↗ Ranking")
            col_d, col_e, col_f = st.columns(3)
            with col_d:
                st.metric("Melhor Trade Possível", f"+{melhor:.1f}%")
            with col_e:
                st.metric("Pior Trade Possível", f"{pior:.1f}%")
            with col_f:
                st.metric("Seu Percentil", f"Top {100 - percentil:.1f}%")

            st.info(f"Seu trade ficou melhor que {percentil:.1f}% de todos os {total:,} trades possíveis com {ticker}.")

            st.subheader("◆ Distribuição de todos os trades possíveis")

            df_hist = pd.DataFrame({"retorno": retornos_validos})

            fig = px.histogram(
                df_hist,
                x="retorno",
                nbins=80,
                labels={"retorno": "Retorno (%)"},
                color_discrete_sequence=["#4a90d9"]
            )

            fig.add_vline(
                x=retorno,
                line_color="#E8FF00",
                line_width=3,
                annotation_text="VOCÊ",
                annotation_font_color="#E8FF00",
                annotation_font_size=14
            )

            fig.update_layout(
                paper_bgcolor="#0A0A0A",
                plot_bgcolor="#0A0A0A",
                font_color="#F2F0E8",
                showlegend=False,
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
            )

            st.plotly_chart(fig, use_container_width=True)
