\# 📊 Real-Time Crypto Analytics Dashboard



A real-time cryptocurrency tracking and analytics platform built with Python, PostgreSQL, and Streamlit. The system continuously fetches live price data from the CoinGecko API, stores it in a PostgreSQL database, and visualizes it through an interactive dashboard with advanced analytics.



\## 🚀 Features



\- \*\*Live Price Tracking\*\* — Real-time prices for 8 major cryptocurrencies (Bitcoin, Ethereum, Solana, etc.)

\- \*\*Auto-Refreshing Dashboard\*\* — Updates every 15 seconds

\- \*\*Top Gainer/Loser Detection\*\* — Automatically identifies best/worst performing coins

\- \*\*Price Alert System\*\* — Flags coins with significant 24h price movement (5%+)

\- \*\*Analytics Summary\*\* — Average, max, min prices computed via SQL

\- \*\*Volatility Score\*\* — Risk assessment using standard deviation

\- \*\*Correlation Analysis\*\* — Heatmap showing how different coins move relative to each other

\- \*\*Trend Prediction\*\* — Short-term trend indication using moving averages

\- \*\*CSV Export\*\* — Download raw data anytime



\## 🛠️ Tech Stack



\- \*\*Python\*\* — Data fetching, processing, and dashboard logic

\- \*\*PostgreSQL\*\* — Database for storing historical price data

\- \*\*Streamlit\*\* — Interactive web dashboard

\- \*\*CoinGecko API\*\* — Live cryptocurrency data source

\- \*\*Pandas\*\* — Data manipulation and analysis



\## 📐 Architecture



CoinGecko API → Python (fetch\_data.py) → PostgreSQL Database → Streamlit Dashboard (dashboard.py)





\- `fetch\_data.py` runs continuously, pulling live prices every 60 seconds and storing them in PostgreSQL

\- `dashboard.py` reads from the database and renders a live, auto-refreshing analytics dashboard



\## ⚙️ Setup Instructions



1\. Clone this repository

2\. Install dependencies:

```bash

&#x20;  pip install psycopg2-binary pandas requests streamlit python-dotenv

```

3\. Create a PostgreSQL database and table:

```sql

&#x20;  CREATE DATABASE crypto\_db;

&#x20;  CREATE TABLE prices (

&#x20;      id SERIAL PRIMARY KEY,

&#x20;      coin VARCHAR(50),

&#x20;      price\_usd NUMERIC,

&#x20;      change\_24h NUMERIC,

&#x20;      timestamp TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

&#x20;  );

```

4\. Create a `.env` file with your database password:



DB\_PASSWORD=your\_password\_here



5\. Run the data fetcher (in one terminal):

```bash

&#x20;  python fetch\_data.py

```

6\. Run the dashboard (in another terminal):

```bash

&#x20;  streamlit run dashboard.py

```



\## 📈 Future Improvements



\- Deploy on cloud for 24/7 availability

\- Add email/SMS alerts for major price movements

\- Expand to stock market data

\- Integrate machine learning for more accurate predictions



\## 👤 Author



Built as a real-time data analytics project to demonstrate skills in API integration, database management, and interactive data visualization.

