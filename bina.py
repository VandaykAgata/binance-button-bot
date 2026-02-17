import requests
import time
import random
import config

# --- 1. Начало ---
TELEGRAM_BOT_TOKEN = config.TOKEN
TELEGRAM_CHAT_ID = config.CHAT_ID
AUTH_COOKIE = config.COOKIE
CSRF_TOKEN = config.CSRF

# --- 2. АВТОРИЗАЦИОННЫЕ ДАННЫЕ ---
PASSTHROUGH_TOKEN = ""

# --- 3. КОНФИГУРАЦИЯ ЗАГОЛОВКОВ ---
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": AUTH_COOKIE,
    "Csrftoken": CSRF_TOKEN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

# --- 4. API ЭНДПОИНТЫ ---
API_INFO_URL = "https://www.binance.com/bapi/composite/v1/public/growth-paas/button-game-activity/game-info"
API_CLICK_URL = "https://www.binance.com/bapi/composite/v1/private/growth-paas/button-game-activity/click-button"


# --- 5. ФУНКЦИИ ---
def send_telegram_notification(message):
    """Отправляет уведомление в Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        # Устанавливаем таймаут, чтобы не зависать при проблемах с сетью Telegram
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        # Выводим в консоль, если не удалось отправить в Telegram
        print(f"Не удалось отправить уведомление в Telegram (проверьте токен/ID): {e}")


def get_game_info():
    """
    Получает текущее время таймера и время последнего клика (для синхронизации)
    с Binance API.
    """
    response = None
    try:
        payload = {"resourceId": 22615}
        response = requests.post(API_INFO_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Вызовет исключение для ошибок 4xx/5xx

        data = response.json().get("data")
        last_clicked_time = data.get("lastClickedTime")  # Время клика с сервера (в мс)

        current_time_ms = time.time() * 1000  # Наше текущее локальное время
        time_elapsed_ms = current_time_ms - last_clicked_time
        time_elapsed_seconds = time_elapsed_ms / 1000
        time_left = 60 - time_elapsed_seconds

        # Возвращаем ТАЙМЕР и СЕРВЕРНОЕ ВРЕМЯ КЛИКА в кортеже
        return max(0, time_left), last_clicked_time

    except requests.exceptions.HTTPError as e:
        if response is not None and response.status_code in [401, 403]:
            send_telegram_notification(
                f"❌ КРИТИЧЕСКАЯ ОШИБКА API: Авторизация провалена! {response.status_code}. Проверьте куки!")
        return None, None
    except requests.exceptions.RequestException:
        return None, None
    except Exception:
        return None, None


def click_the_button():
    """Выполняет клик по кнопке Binance для сброса таймера."""
    # Рандомизированная человеческая задержка
    # В режиме "Страховка" - сохраняем. В режиме "Победа" - закомментируйте эти 2 строки.
    human_delay = random.uniform(0.05, 0.10)
    time.sleep(human_delay)
    print(f"Попытка нажать на кнопку после задержки {human_delay:.2f} сек...")

    response = None
    try:
        payload = {"resourceId": 22615}
        response = requests.post(API_CLICK_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        print(f"Результат клика: {result}")
        return result.get("success", False)

    except requests.exceptions.HTTPError as e:
        if response is not None and response.status_code in [401, 403]:
            send_telegram_notification(
                f"❌ КРИТИЧЕСКАЯ ОШИБКА: Авторизация провалена! {response.status_code}. Обновите токены!")
        return False
    except Exception:
        return False


# --- ГЛАВНЫЙ ЦИКЛ НАБЛЮДЕНИЯ И СБРОСА ---
notification_sent = False
click_attempted = False

# --- 💡 ВАШ ВЫБОР РЕЖИМА ---
# 35: Режим Страховки (бот кликнет, чтобы не проиграть).
# 0:  Режим Боя (бот не кликнет, вы кликаете сами в 00:00).
SAFE_RESET_THRESHOLD = 40

# --- ПЕРЕМЕННЫЕ ДЛЯ ПРОВЕРКИ "ПУЛЬСА" (КАЖДЫЕ 6 ЧАСОВ) ---
HEARTBEAT_INTERVAL_SECONDS = 21600
last_heartbeat_time = time.time()

while True:

    # ПРИНИМАЕМ ДВА ЗНАЧЕНИЯ: ТАЙМЕР И СЕРВЕРНОЕ ВРЕМЯ
    timer_seconds, server_last_click_time = get_game_info()
    current_time = time.time()

    if timer_seconds is not None:

        # ----------------------------------------------------
        # --- ЛОГИКА "ПУЛЬСА" ---
        # ----------------------------------------------------
        if current_time - last_heartbeat_time >= HEARTBEAT_INTERVAL_SECONDS:
            send_telegram_notification("💚 ПУЛЬС БОТА: Я активен и слежу за таймером.")
            last_heartbeat_time = current_time
            print(">>> Отправлен 'Пульс' бота (работает).")
        # ----------------------------------------------------

        # Если таймер сбросился (60 секунд), сбрасываем флаги для нового цикла
        if timer_seconds > 59:
            notification_sent = False
            click_attempted = False
            print(f"--- НОВЫЙ ЦИКЛ. Таймер сброшен: {timer_seconds:.2f} сек. ---")

        print(f"Текущий таймер: {timer_seconds:.2f} сек. | Порог сброса: {SAFE_RESET_THRESHOLD:.2f} сек.")

        # УСЛОВИЕ ДЛЯ СТРАХОВОЧНОГО СБРОСА
        if timer_seconds < SAFE_RESET_THRESHOLD:

            # 1. УВЕДОМЛЕНИЕ
            if not notification_sent:
                message = (
                    f"📢 ВНИМАНИЕ! Таймер достиг критического значения: {timer_seconds:.2f} сек. "
                    f"Бот выполнит безопасный сброс, чтобы дать вам время."
                )
                print(message)
                send_telegram_notification(message)
                notification_sent = True

            # 2. АВТОКЛИК (СБРОС)
            if not click_attempted:

                success = click_the_button()

                if success:
                    send_telegram_notification(
                        f"✅ БЕЗОПАСНЫЙ СБРОС УСПЕШЕН! Время: {timer_seconds:.2f} сек. Таймер сброшен до 60, можете брать управление."
                    )
                else:
                    send_telegram_notification(
                        f"❌ БЕЗОПАСНЫЙ СБРОС НЕ УДАЛСЯ. Время: {timer_seconds:.2f} сек. Проверьте токены!"
                    )

                click_attempted = True

        # --- РАНДОМИЗИРОВАННАЯ ПАУЗА (Оптимизирована для скорости) ---
        sleep_time = random.uniform(0.2, 0.5)
        time.sleep(sleep_time)

    else:
        # Если API не отвечает
        print("❌ ОШИБКА API: Не удалось получить данные. Ожидание 5.0 сек.")
        time.sleep(5.0)