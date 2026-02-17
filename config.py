import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SAFE_RESET_THRESHOLD = 40  # Вынесли настройку сюда

# Собираем заголовки один раз, чтобы не мусорить в основном коде
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": os.getenv("COOKIE"),
    "Csrftoken": os.getenv("CSRF"),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

API_INFO_URL = "https://www.binance.com/bapi/composite/v1/public/growth-paas/button-game-activity/game-info"
API_CLICK_URL = "https://www.binance.com/bapi/composite/v1/private/growth-paas/button-game-activity/click-button"