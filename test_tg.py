import requests
import config # Импортируем наш центральный конфиг

# Берем данные из config.py, который в свою очередь берет их из .env
TOKEN = config.TOKEN
CHAT_ID = config.CHAT_ID

def send_test_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status() # Проверка, что запрос прошел успешно (код 200)
        print("✅ Тестовое уведомление успешно отправлено.")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")

if __name__ == "__main__":
    send_test_message("🚀 Тестовое сообщение: связь с ботом установлена!")