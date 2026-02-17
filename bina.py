import requests
import time
import random
from config import TOKEN, CHAT_ID, HEADERS, API_INFO_URL, API_CLICK_URL, SAFE_RESET_THRESHOLD


def send_notification(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except Exception as e:
        print(f"TG Error: {e}")


def get_timer():
    try:
        response = requests.post(API_INFO_URL, json={"resourceId": 22615}, headers=HEADERS)
        last_click = response.json()['data']['lastClickedTime']
        time_left = 60 - ((time.time() * 1000 - last_click) / 1000)
        return max(0, time_left)
    except:
        return None


def click():
    time.sleep(random.uniform(0.05, 0.1))
    try:
        res = requests.post(API_CLICK_URL, json={"resourceId": 22615}, headers=HEADERS)
        return res.json().get("success", False)
    except:
        return False


# Основной цикл
notification_sent = click_done = False

while True:
    timer = get_timer()
    if timer is not None:
        if timer > 59:
            notification_sent = click_done = False

        print(f"Таймер: {timer:.2f} сек.")

        if timer < SAFE_RESET_THRESHOLD:
            if not notification_sent:
                send_notification(f"⚠️ Порог {SAFE_RESET_THRESHOLD}с пройден! Сбрасываю...")
                notification_sent = True
            if not click_done:
                if click():
                    send_notification("✅ Сброшено успешно!")
                click_done = True

        time.sleep(random.uniform(0.3, 0.6))
    else:
        time.sleep(5)