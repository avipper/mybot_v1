# bot.py
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("8380395268:AAHcRYxmenMO8WHfgJcC8Y-dESeZgwxrUYY")  # токен от BotFather
WEBHOOK_HOST = os.getenv("https://mybot-v1-2u8v.onrender.com")  # URL Render, например https://my-tg-bot.onrender.com
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот на Render через webhook 🚀")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

app = web.Application()
app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

async def handle(request):
    update = await request.json()
    telegram_update = types.Update.to_object(update)
    await dp.process_update(telegram_update)
    return web.Response()

app.router.add_post(WEBHOOK_PATH, handle)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    web.run_app(app, host="0.0.0.0", port=port)
