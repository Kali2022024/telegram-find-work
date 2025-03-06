from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from telethon import TelegramClient, events
import asyncio
import os

# Конфігурація
API_TOKEN = ""
TELEGRAM_API_ID = ""
TELEGRAM_API =" "
CHANNELS_TO_MONITOR = [
    "https://t.me/+XG0-Pv2XBzFmOWQ6",
    "https://t.me/workua_remote",
    "https://t.me/RABOTA_KIEVO",
    "https://t.me/+Og_VYe0Eww02N2My",
    "https://t.me/rabota_robota_ua",
    "https://t.me/robotaua_now_remote",
    "https://t.me/ua_robota",
    "https://t.me/rabota_robota_ua0",
    "https://t.me/+IFWv1op6Hwc1NGEy",
    "https://t.me/fffifiif"
        # Список каналів через посилання
] 
CRITERIA = ["Python", "Remote", "20000", "20.000", "Віддалено","$","Агенство","30 000","30000","30.000","40.000","40000","40 000", "Crypto", "Крипта","Криптовалюта","Чаттер","ОнлиФанс","Онліфанс","onlyfans","OnlyFans","Onlyfans","4 години", "18:00"]  # Ключові слова
YOUR_TELEGRAM_USER_ID =

# Ініціалізація бота та клієнта
bot = Bot(token=API_TOKEN)  
dp = Dispatcher() 
session_file = "monitoring_session_v2"
if os.path.exists(session_file + '.session'):
    os.remove(session_file + '.session')  # Видаляємо стару сесію перед запуском
client = TelegramClient(session_file, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def send_notification(post_link, message):
    try:
        await bot.send_message(
            chat_id=YOUR_TELEGRAM_USER_ID,
            text=f"Знайдена вакансія:\n\n{message}\n\nПосилання: {post_link}",
        )
    except Exception as e:
        print(f"Помилка надсилання повідомлення: {e}")

# Обробка нових постів у Telethon
@client.on(events.NewMessage())
async def handle_new_post(event):
    try:
        # Перевірка, чи канал відповідає посиланню
        if event.chat and event.chat.username:
            for channel_link in CHANNELS_TO_MONITOR:
                if f"t.me/{event.chat.username}" == channel_link.replace('https://', '').replace('http://', ''):
                    message_text = event.message.text  
                    print(f"Отримано повідомлення: {message_text}")  # Для журналювання
                    if any(keyword.lower() in message_text.lower() for keyword in CRITERIA):
                        post_link = f"https://t.me/{event.chat.username}/{event.message.id}"
                        print(f"Повідомлення містить ключові слова, надсилаємо сповіщення: {post_link}")
                        await send_notification(post_link, message_text)
    except Exception as e:
        print(f"Помилка обробки нового повідомлення: {e}")

# Обробка команди /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Цей бот моніторить вакансії на заданих каналах. Ви отримаєте сповіщення про відповідні пости.")

# Головна функція
async def main():
    # Запуск Telethon
    await client.start()
    print("Telegram Monitoring Bot запущено!")

    # Запуск aiogram
    asyncio.create_task(dp.start_polling(bot))

    # Утримання Telethon у роботі
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
