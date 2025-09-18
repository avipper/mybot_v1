import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("BOT_TOKEN") # Получение токена из переменных окружения
# WEBHOOK_HOST = os.getenv("WEBHOOK_HOST") # URL Render, например https://my-tg-bot.onrender.com
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")  # Render подставляет URL автоматически

# Проверка наличия токена
if not API_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена! Установите токен от BotFather.")

# Проверка наличия url
if not WEBHOOK_HOST:
    raise ValueError("Переменная окружения WEBHOOK_HOST не установлена!")

WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот на Render через webhook 🚀")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def on_startup(app):
    # Устанавливаем webhook
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    # Закрываем соединение с Telegram
    await bot.delete_webhook()
    await bot.session.close()


async def handle(request):
    data = await request.json()

    from aiogram import types
    update = types.Update(**data)

    # ВАЖНО: задаём текущий bot
    from aiogram import Bot
    Bot.set_current(bot)

    await dp.process_update(update)
    return web.Response()


def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()



