import os
import subprocess
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Telegram Bot Token
BOT_TOKEN = "7264046798:AAHvUOtdwjvRyzLugAZ_WS5xT6nt1pKVB1M"

# Администраторские ID
ADMIN_IDS = [1112129981, 1478056340]  # Замените на ваши Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(BOT_TOKEN)

# Пути к скриптам
SCRIPT_PATHS = [
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\1.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\2.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\3.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\4.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\5.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\6.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\7.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\8.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\9.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\10.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\11.py",
    "C:\\Users\\kira\\Desktop\\code\\captcha\\tg\\12.py"
]

# Глобальный список для хранения запущенных процессов
processes = []

def start_scripts():
    """Запускает все скрипты в отдельных процессах."""
    global processes

    if processes:
        return "\u26a0\ufe0f Скрипты уже запущены."

    try:
        for script in SCRIPT_PATHS:
            if not os.path.exists(script):
                logging.warning(f"Скрипт не найден: {script}")
                continue

            process = subprocess.Popen(["python", script], creationflags=subprocess.CREATE_NEW_CONSOLE)
            processes.append(process)
        return "\u2705 Все доступные скрипты успешно запущены."
    except Exception as e:
        logging.error(f"Ошибка при запуске скриптов: {e}")
        return f"\u274c Ошибка при запуске скриптов: {e}"

def stop_scripts():
    """Останавливает все запущенные процессы."""
    global processes

    if not processes:
        return "\u26a0\ufe0f Скрипты не запущены."

    try:
        for process in processes:
            process.terminate()
        processes = []
        return "\u2705 Все скрипты успешно остановлены."
    except Exception as e:
        logging.error(f"Ошибка при остановке скриптов: {e}")
        return f"\u274c Ошибка при остановке скриптов: {e}"

def get_status():
    """Проверяет состояние запущенных скриптов."""
    if not processes:
        return "\u26a0\ufe0f Скрипты не запущены."

    status = "\u2705 Запущенные скрипты:\n"
    for i, process in enumerate(processes, start=1):
        status += f"{i}. PID: {process.pid}\n"
    return status

@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "\u274c Доступ запрещен.")
        logging.warning(f"Неавторизованный доступ: {message.from_user.id}")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("\u25b6\ufe0f Запустить скрипты")
    stop_button = KeyboardButton("\u23f9\ufe0f Остановить скрипты")
    status_button = KeyboardButton("\ud83d\udd0d Проверить статус")
    markup.add(start_button, stop_button, status_button)

    bot.reply_to(message, "\ud83d\ude4b\u200d Добро пожаловать! Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "\u25b6\ufe0f Запустить скрипты")
def handle_start(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "\u274c Доступ запрещен.")
        logging.warning(f"Неавторизованный доступ: {message.from_user.id}")
        return

    result = start_scripts()
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "\u23f9\ufe0f Остановить скрипты")
def handle_stop(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "\u274c Доступ запрещен.")
        logging.warning(f"Неавторизованный доступ: {message.from_user.id}")
        return

    result = stop_scripts()
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "\ud83d\udd0d Проверить статус")
def handle_status(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "\u274c Доступ запрещен.")
        logging.warning(f"Неавторизованный доступ: {message.from_user.id}")
        return

    result = get_status()
    bot.reply_to(message, result)

if __name__ == "__main__":
    logging.info("Бот запущен и готов к работе.")
    bot.infinity_polling()
