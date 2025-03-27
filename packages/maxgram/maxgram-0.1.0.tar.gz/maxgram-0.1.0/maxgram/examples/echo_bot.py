#!/usr/bin/env python
"""
Пример простого эхо-бота, который отвечает на команды и повторяет сообщения пользователя.
"""

import os
import logging
import asyncio

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Импортируем библиотеку
from maxgram import Bot

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Если токен не указан
if not BOT_TOKEN:
    BOT_TOKEN = "YOUR_BOT_TOKEN"  # Замените на свой токен
    logging.warning("Токен бота не указан. Используйте переменную окружения BOT_TOKEN")

# Создаем экземпляр бота
bot = Bot(BOT_TOKEN)

# Обработчик ошибок
@bot.catch
async def error_handler(err, ctx):
    logging.error(f"Произошла ошибка: {err}")
    await ctx.reply("Произошла ошибка при обработке вашего запроса.")
    # Не завершаем работу программы

# Обработчик команды /start
@bot.command("start")
async def start_command(ctx):
    await ctx.reply("Привет! Я эхо-бот. Напиши мне что-нибудь, и я отправлю это в ответ.")

# Обработчик команды /help
@bot.command("help")
async def help_command(ctx):
    await ctx.reply(
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Показать эту справку\n\n"
        "Просто отправьте любое сообщение, и я повторю его."
    )

# Обработчик для всех текстовых сообщений
@bot.on("message_created")
async def echo(ctx):
    if ctx.message and hasattr(ctx.message.body, "text") and ctx.message.body.text:
        # Игнорируем команды (сообщения, начинающиеся с /)
        if not ctx.message.body.text.startswith('/'):
            await ctx.reply(ctx.message.body.text)

# Запуск бота
if __name__ == "__main__":
    logging.info("Запуск бота...")
    
    # Запускаем бота
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        logging.info("Остановка бота...")
        bot.stop()
    finally:
        loop.close() 