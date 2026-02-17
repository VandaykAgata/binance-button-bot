import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
COOKIE = os.getenv("COOKIE")
CSRF = os.getenv("CSRF")