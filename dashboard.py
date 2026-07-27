from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
import psycopg2
import pandas as pd
import time

DB_URL = os.getenv("DB_URL")

st.set_page_config(page_title="Crypto Live Dashboard", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #1c1f26;
        border: 1px solid #2d3139;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Real-Time Crypto Analytics Dashboard")
st.caption("Live data from CoinGecko API • Auto-updates every 15 seconds")

placeholder = st.empty()
REFRESH_SECONDS = 15

while True:
    conn = psycopg2.connect(DB_URL)
    df = pd.read_sql("SELECT * FROM prices ORDER BY timestamp DESC LIMIT 1000", conn)
    conn.close()

    with placeholder.container():
        latest = df.sort_values("timestamp").groupby("coin").tail(1).reset_index(drop=True)

        # ---- ALERT SYSTEM ----
        alerts = latest[latest["change_24h"].abs() >= 5]
        if not alerts.empty:
            for _, row in alerts.iterrows():
                direction = "🚀 surged" if row["change_24h"] > 0 else "⚠️ dropped"
                st.warning(f"**{row['coin'].upper()}** has {direction} by {row['change_24h']:.2f}% in 24h!")

        # ---- METRIC CARDS ----
        st.subheader("💰 Live Prices")
        cols = st.columns(len(latest))
        for i, row in latest.iterrows():
            with cols[i]:
                st.metric(
                    label=row["coin"].upper(),
                    value=f"${row['price_usd']:,.2f}",
                    delta=f"{row['change_24h']:.2f}%"
                )

        st.divider()

        # ---- TOP GAINER / LOSER ----
        col1, col2 = st.columns(2)
        top_gainer = latest.loc[latest["change_24h"].idxmax()]
        top_loser = latest.loc[latest["change_24h"].idxmin()]

        with col1:
            st.success(f"🚀 Top Gainer: **{top_gainer['coin'].upper()}** ({top_gainer['change_24h']:.2f}%)")
        with col2:
            st.error(f"📉 Top Loser: **{top_loser['coin'].upper()}** ({top_loser['change_24h']:.2f}%)")

        st.divider()

        # ---- PRICE TREND CHART ----
        st.subheader("📈 Price Trend")
        pivot_df = df.pivot_table(index="timestamp", columns="coin", values="price_usd")
        st.line_chart(pivot_df)

        st.divider()

        # ---- ANALYTICS TABLE ----
        st.subheader("📊 Analytics Summary")
        conn = psycopg2.connect(DB_URL)
        analytics_query = """
            SELECT 
                coin,
                ROUND(AVG(price_usd)::numeric, 2) AS avg_price,
                ROUND(MAX(price_usd)::numeric, 2) AS max_price,
                ROUND(MIN(price_usd)::numeric, 2) AS min_price,
                COUNT(*) AS data_points
            FROM prices
            GROUP BY coin
            ORDER BY avg_price DESC;
        """
        analytics_df = pd.read_sql(analytics_query, conn)
        conn.close()
        st.dataframe(analytics_df, use_container_width=True)

        st.divider()

        # ---- VOLATILITY SCORE ----
        st.subheader("⚡ Volatility Score (Risk Level)")
        conn = psycopg2.connect(DB_URL)
        volatility_query = """
            SELECT 
                coin,
                ROUND(STDDEV(price_usd)::numeric, 4) AS volatility,
                ROUND(AVG(price_usd)::numeric, 2) AS avg_price
            FROM prices
            GROUP BY coin
            ORDER BY volatility DESC;
        """
        volatility_df = pd.read_sql(volatility_query, conn)
        conn.close()

        volatility_df["volatility"] = volatility_df["volatility"].fillna(0)
        median_volatility = volatility_df["volatility"].median()
        volatility_df["risk_level"] = volatility_df["volatility"].apply(
            lambda x: "🔴 High" if x > median_volatility else "🟢 Low"
        )
        st.dataframe(volatility_df, use_container_width=True)

        st.divider()

        # ---- CORRELATION ANALYSIS ----
        st.subheader("🔗 Price Correlation Between Coins")
        st.caption("Values close to 1 mean coins move together. Close to -1 means they move opposite.")
        correlation_df = pivot_df.corr()
        st.dataframe(correlation_df.style.background_gradient(cmap="RdYlGn", vmin=-1, vmax=1), use_container_width=True)

        st.divider()

        # ---- PREDICTIVE TREND (Moving Average) ----
        st.subheader("🔮 Short-Term Trend Prediction")
        st.caption("Based on moving averages — indicates likely short-term direction, not financial advice.")

        prediction_data = []
        for coin in pivot_df.columns:
            coin_prices = pivot_df[coin].dropna()
            if len(coin_prices) >= 5:
                ma_short = coin_prices.tail(3).mean()
                ma_long = coin_prices.tail(10).mean() if len(coin_prices) >= 10 else coin_prices.mean()

                if ma_short > ma_long:
                    trend = "📈 Likely Upward"
                elif ma_short < ma_long:
                    trend = "📉 Likely Downward"
                else:
                    trend = "➡️ Stable"

                prediction_data.append({
                    "coin": coin,
                    "recent_avg": round(ma_short, 2),
                    "longer_avg": round(ma_long, 2),
                    "predicted_trend": trend
                })

        if prediction_data:
            prediction_df = pd.DataFrame(prediction_data)
            st.dataframe(prediction_df, use_container_width=True)
        else:
            st.info("Collecting more data for predictions... check back in a few minutes.")

        st.divider()

        # ---- DOWNLOAD BUTTON ----
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Data as CSV", data=csv, file_name="crypto_data.csv", mime="text/csv", key=f"download_{time.time()}")

        countdown_placeholder = st.empty()

    for remaining in range(REFRESH_SECONDS, 0, -1):
        countdown_placeholder.caption(f"⏳ Next update in {remaining} seconds...")
        time.sleep(1)