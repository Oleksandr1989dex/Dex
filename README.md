# Dexchiterbot

**Dexchiterbot** — це Telegram-бот, який щохвилини відстежує нові токени на DEX-платформах через [dexscreener.com](https://dexscreener.com), перевіряє їх на наявність торгів на MEXC і Binance, та надсилає повідомлення, якщо виконуються такі умови:

- Токен торгується на MEXC;
- Токен не торгується на Binance;
- Різниця в ціні між DEX та MEXC перевищує 7%.

## Функціонал

- Моніторинг нових токенів на DEX через DexScreener API
- Перевірка присутності токену на MEXC та Binance
- Визначення цінової різниці між DEX та CEX
- Повідомлення у Telegram через бота

## Технології

- Python 3
- `aiohttp` — асинхронні HTTP-запити
- `telebot` або `aiogram` — Telegram-бот
- `apscheduler` — періодичні завдання
- Railway — хостинг

## Налаштування

1. Клонуй репозиторій:
   ```bash
   git clone https://github.com/ТВОЄ-ІМʼЯ-КОРИСТУВАЧА/Dexchiterbot.git
   cd Dexchiterbot
