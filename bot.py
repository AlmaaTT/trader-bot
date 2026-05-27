import yfinance as yf
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
TOKEN = "8781391896:AAH9dNTYHtx0Qj6BVCSaFMz_qRtvZuuOOVY"
#TOKEN = os.environ.get("TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
print(f"TOKEN получен: {TOKEN is not None}")  # добавь эту строку


client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)


def get_market_data():
    stocks = {"Apple": "AAPL", "Tesla": "TSLA", "Microsoft": "MSFT"}
    pairs = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "DXY": "DX-Y.NYB"}

    data = "Акции:\n"
    for name, ticker in stocks.items():
        price = yf.Ticker(ticker).fast_info.last_price
        data += f"{name}: ${price:.2f}\n"

    data += "\nВалюты:\n"
    for name, ticker in pairs.items():
        price = yf.Ticker(ticker).fast_info.last_price
        data += f"{name}: {price:.5f}\n"

    return data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой торговый ИИ-помощник 🤖\n\n"
        "Команды:\n"
        "/stocks — данные по акциям\n"
        "/currency — курсы валют\n"
        "/analyze — ИИ анализ рынка"
    )


async def stocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tickers = {"Apple": "AAPL", "Tesla": "TSLA", "Microsoft": "MSFT"}
    msg = "📈 Акции:\n\n"
    for name, ticker in tickers.items():
        price = yf.Ticker(ticker).fast_info.last_price
        msg += f"{name}: ${price:.2f}\n"
    await update.message.reply_text(msg)


async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pairs = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "DXY": "DX-Y.NYB"}
    msg = "💱 Валюты:\n\n"
    for name, ticker in pairs.items():
        price = yf.Ticker(ticker).fast_info.last_price
        msg += f"{name}: {price:.5f}\n"
    await update.message.reply_text(msg)


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Анализирую рынок, подожди...")

    market_data = get_market_data()

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Ты опытный трейдер. Вот текущие рыночные данные:

{market_data}

Дай краткий анализ на русском языке:
1. Общая картина рынка
2. По каждой валютной паре: купить/продать/держать и почему
3. По акциям: общий тренд
4. Главный совет на сегодня

Будь конкретным и кратким."""
        }]
    )

    analysis = message.content[0].text
    await update.message.reply_text(f"🤖 ИИ Анализ:\n\n{analysis}")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stocks", stocks))
    app.add_handler(CommandHandler("currency", currency))
    app.add_handler(CommandHandler("analyze", analyze))
    app.run_polling()


if __name__ == "__main__":
    main()