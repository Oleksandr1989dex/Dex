
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Токен DEX Screener API
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен Telegram бота
CHAT_ID = os.getenv("CHAT_ID")      # ID чату, куди слати повідомлення

def get_tokens_from_dexscreener():
    url = "https://api.dexscreener.com/latest/dex/pairs/mexc"
    headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("pairs", [])
    return []

def get_binance_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        symbols = [s['symbol'].lower() for s in response.json()['symbols']]
        return symbols
    return []

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def filter_tokens(pairs, binance_symbols):
    filtered = []
    for pair in pairs:
        symbol = (pair.get("baseToken", {}).get("symbol", "") + pair.get("quoteToken", {}).get("symbol", "")).lower()
        if symbol not in binance_symbols:
            price_dex = float(pair.get("priceUsd", 0))
            price_cex = float(pair.get("priceNative", 0))
            if price_dex and price_cex:
                difference = abs(price_dex - price_cex) / min(price_dex, price_cex)
                if difference >= 0.07:
                    filtered.append((symbol.upper(), price_dex, price_cex, difference))
    return filtered

def main_loop():
    while True:
        try:
            pairs = get_tokens_from_dexscreener()
            binance_symbols = get_binance_symbols()
            filtered = filter_tokens(pairs, binance_symbols)

            for token in filtered:
                symbol, dex_price, mexc_price, diff = token
                msg = f"<b>{symbol}</b>\nDEX: ${dex_price:.4f}\nMEXC: ${mexc_price:.4f}\nDifference: {diff * 100:.2f}%"
                send_telegram_message(msg)

        except Exception as e:
            send_telegram_message(f"Помилка в боті: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
