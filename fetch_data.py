from dotenv import load_dotenv
import os
load_dotenv()

import requests
import psycopg2
from datetime import datetime
import time

DB_URL = os.getenv("DB_URL")

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,dogecoin,solana,cardano,ripple,polkadot,litecoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params)
    return response.json()

def save_to_postgres(data):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    for coin, values in data.items():
        cur.execute(
            "INSERT INTO prices (coin, price_usd, change_24h, timestamp) VALUES (%s, %s, %s, %s)",
            (coin, values["usd"], values.get("usd_24h_change", 0), datetime.now())
        )
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    while True:
        data = fetch_crypto_data()
        save_to_postgres(data)
        print(f"✅ Data saved at {datetime.now()}")
        time.sleep(60)