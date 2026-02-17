🚀 Binance Button Game Automator

Description: A Python-based automation tool for the Binance Button Game. The bot monitors the game timer in real-time and performs a "safety click" to prevent losing when the timer reaches a critical threshold.

✨ Key Features:
Real-time Monitoring: Tracks the countdown timer via Binance internal API.

Smart Reset: Automatically resets the timer based on a customizable threshold.

Telegram Notifications: Sends instant alerts and "heartbeat" status updates to your phone.

Human-like Behavior: Implements randomized delays to mimic human interaction.

Secure: Uses environment variables (.env) to handle sensitive session data and tokens.

🛠 Tech Stack:
Language: Python 3.10+

Libraries: requests for API interaction, python-dotenv for security.

Automation: Real-time polling with randomized intervals.

Русская версия

Описание: Автоматизированный инструмент на Python для участия в игре «Binance Button Game». Бот в реальном времени следит за игровым таймером и выполняет «страховочный клик», если время достигает критического порога, предотвращая проигрыш.

✨ Основные функции:
Мониторинг в реальном времени: Отслеживание обратного отсчета через внутреннее API Binance.

Умный сброс: Автоматическое нажатие кнопки при достижении заданного лимита времени (например, 40 секунд).

Telegram-уведомления: Мгновенные оповещения о действиях бота и «пульс» (heartbeat), подтверждающий, что бот активен.

Эмуляция поведения пользователя: Использование рандомизированных задержек для имитации действий человека.

Безопасность: Использование переменных окружения (.env) для защиты токенов и сессионных данных.

🛠 Технологический стек:
Язык: Python 3.10+

Библиотеки: requests (API взаимодействие), python-dotenv (безопасность).

Методология: Анализ сетевого трафика (Network inspection) для взаимодействия с закрытыми эндпоинтами.