#!/usr/bin/env python
"""
Пример использования интерактивных клавиатур в боте.
"""

import os
import logging
import asyncio

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Импортируем библиотеку
from maxgram import Bot
from maxgram.core.helpers.keyboard import button, inline_keyboard

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Если токен не указан
if not BOT_TOKEN:
    BOT_TOKEN = "YOUR_BOT_TOKEN"  # Замените на свой токен
    logging.warning("Токен бота не указан. Используйте переменную окружения BOT_TOKEN")

# Создаем экземпляр бота
bot = Bot(BOT_TOKEN)

# Устанавливаем команды бота
bot.api.set_my_commands([
    {"name": "start", "description": "Начать взаимодействие с ботом"},
    {"name": "menu", "description": "Показать основное меню"},
    {"name": "callback", "description": "Демонстрация callback-кнопок"},
    {"name": "location", "description": "Запросить геолокацию"},
    {"name": "contact", "description": "Запросить контакт"},
])

# Стандартные кнопки, которые будут добавлены ко всем клавиатурам
default_buttons = [
    [button.link("❤️ Документация", "https://dev.max.ru/")],
    [button.callback("Удалить сообщение", "remove_message", {"intent": "negative"})],
]

# Обработчик для удаления сообщения
@bot.action("remove_message")
async def remove_message_handler(ctx):
    result = await ctx.delete_message()
    
    await ctx.answer_on_callback({
        "notification": "Сообщение удалено" if result.get("success", False) else "Не удалось удалить сообщение"
    })

# Обработчик команды /start
@bot.command("start")
async def start_command(ctx):
    await ctx.reply(
        "Привет! Я демонстрационный бот для показа возможностей интерактивных клавиатур. "
        "Используйте команду /menu для просмотра основного меню."
    )

# Обработчик команды /menu
@bot.command("menu")
async def menu_command(ctx):
    # Создаем клавиатуру с основными функциями
    keyboard = inline_keyboard([
        [
            button.callback("Callback кнопки", "show_callbacks"),
            button.callback("Запрос локации", "show_location")
        ],
        [
            button.callback("Запрос контакта", "show_contact"),
            button.callback("О боте", "about")
        ],
        *default_buttons
    ])
    
    await ctx.reply("Выберите действие:", {
        "attachments": [keyboard.to_dict()]
    })

# Обработчики для кнопок основного меню
@bot.action("show_callbacks")
async def show_callbacks_handler(ctx):
    await ctx.answer_on_callback({
        "message": {
            "text": "Демонстрация callback-кнопок",
            "attachments": [get_callback_keyboard()]
        }
    })

@bot.action("show_location")
async def show_location_handler(ctx):
    await ctx.answer_on_callback({
        "message": {
            "text": "Демонстрация запроса геолокации",
            "attachments": [get_location_keyboard()]
        }
    })

@bot.action("show_contact")
async def show_contact_handler(ctx):
    await ctx.answer_on_callback({
        "message": {
            "text": "Демонстрация запроса контакта",
            "attachments": [get_contact_keyboard()]
        }
    })

@bot.action("about")
async def about_handler(ctx):
    await ctx.answer_on_callback({
        "message": {
            "text": "Этот бот демонстрирует работу с интерактивными клавиатурами в Max Bot API.\n\n"
                   "Исходный код: https://github.com/max-messenger/maxbot-api-python",
            "attachments": [inline_keyboard([*default_buttons]).to_dict()]
        }
    })

# Функция для создания клавиатуры с callback-кнопками
def get_callback_keyboard():
    return inline_keyboard([
        [
            button.callback("Стандартная", "color:default"),
            button.callback("Позитивная", "color:positive", {"intent": "positive"}),
            button.callback("Негативная", "color:negative", {"intent": "negative"})
        ],
        [
            button.callback("Назад", "back_to_menu")
        ],
        *default_buttons
    ])

# Обработчик callback-кнопок с цветами
@bot.action("color:(.*)")
async def color_handler(ctx):
    color = ctx.match.group(1) if ctx.match else "неизвестный"
    
    await ctx.answer_on_callback({
        "notification": f"Вы выбрали цвет: {color}"
    })

# Функция для создания клавиатуры с запросом геолокации
def get_location_keyboard():
    return inline_keyboard([
        [
            button.request_geo_location("Отправить мою геолокацию")
        ],
        [
            button.callback("Назад", "back_to_menu")
        ],
        *default_buttons
    ])

# Обработчик получения геолокации
@bot.on("message_created")
async def location_handler(ctx, next_fn):
    if ctx.location:
        await ctx.reply(
            f"Получена геолокация:\n"
            f"Широта: {ctx.location['latitude']}\n"
            f"Долгота: {ctx.location['longitude']}"
        )
        return
    
    # Если это не геолокация, передаем управление следующему обработчику
    await next_fn()

# Функция для создания клавиатуры с запросом контакта
def get_contact_keyboard():
    return inline_keyboard([
        [
            button.request_contact("Отправить мой контакт")
        ],
        [
            button.callback("Назад", "back_to_menu")
        ],
        *default_buttons
    ])

# Обработчик получения контакта
@bot.on("message_created")
async def contact_handler(ctx, next_fn):
    if ctx.contact_info:
        full_name = ctx.contact_info.get('fullName', 'Не указано')
        phone = ctx.contact_info.get('tel', 'Не указано')
        
        await ctx.reply(
            f"Получен контакт:\n"
            f"Имя: {full_name}\n"
            f"Телефон: {phone}"
        )
        return
    
    # Если это не контакт, передаем управление следующему обработчику
    await next_fn()

# Обработчик кнопки "Назад"
@bot.action("back_to_menu")
async def back_to_menu_handler(ctx):
    # Возвращаемся в главное меню
    await menu_command(ctx)

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