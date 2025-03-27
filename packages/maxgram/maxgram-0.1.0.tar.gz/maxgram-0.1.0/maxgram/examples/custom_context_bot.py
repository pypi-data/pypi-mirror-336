#!/usr/bin/env python
"""
Пример использования пользовательского контекста для хранения данных сессии.
"""

import os
import logging
import asyncio
from typing import Dict, Optional

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Импортируем библиотеку
from maxgram import Bot, Context
from maxgram.bot import BotConfig

# Глобальное хранилище сессий
session_storage: Dict[int, Dict] = {}

class SessionContext(Context):
    """
    Пользовательский контекст с поддержкой сессий
    """
    
    def __init__(self, update, api, bot_info=None):
        super().__init__(update, api, bot_info)
        
        # Получаем ID пользователя из сообщения или callback
        self.user_id = self._extract_user_id()
        
        # Инициализируем сессию
        if self.user_id:
            if self.user_id not in session_storage:
                session_storage[self.user_id] = {}
            self.session = session_storage[self.user_id]
        else:
            # Если не удалось получить ID пользователя, создаем пустую сессию
            self.session = {}
    
    def _extract_user_id(self) -> Optional[int]:
        """
        Извлекает ID пользователя из обновления
        """
        if self.update.update_type == 'message_created' and self.message and hasattr(self.message, 'from_user'):
            return self.message.from_user.get('id')
        
        if self.update.update_type == 'message_callback' and hasattr(self.update.callback, 'from_user'):
            return self.update.callback.from_user.get('id')
            
        return None
    
    def get_session_value(self, key: str, default=None):
        """
        Получает значение из сессии
        """
        return self.session.get(key, default)
    
    def set_session_value(self, key: str, value):
        """
        Устанавливает значение в сессии
        """
        self.session[key] = value
        return True
    
    def increment_counter(self, key: str, amount: int = 1):
        """
        Увеличивает счетчик в сессии
        """
        current_value = self.get_session_value(key, 0)
        self.set_session_value(key, current_value + amount)
        return current_value + amount
    
    def clear_session(self):
        """
        Очищает сессию пользователя
        """
        if self.user_id:
            session_storage[self.user_id] = {}
            self.session = {}
            return True
        return False

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Если токен не указан
if not BOT_TOKEN:
    BOT_TOKEN = "YOUR_BOT_TOKEN"  # Замените на свой токен
    logging.warning("Токен бота не указан. Используйте переменную окружения BOT_TOKEN")

# Создаем конфигурацию с пользовательским контекстом
config = BotConfig(context_type=SessionContext)

# Создаем экземпляр бота
bot = Bot(BOT_TOKEN, config)

# Обработчик команды /start
@bot.command("start")
async def start_command(ctx):
    # Сохраняем время первого запуска
    first_start = ctx.get_session_value('first_start')
    if not first_start:
        ctx.set_session_value('first_start', ctx.update.timestamp)
        
    # Увеличиваем счетчик запусков
    starts_count = ctx.increment_counter('starts_count')
    
    await ctx.reply(
        f"Привет! Вы запустили бота {starts_count} раз.\n"
        f"Используйте команду /stats для просмотра статистики."
    )

# Обработчик команды /stats
@bot.command("stats")
async def stats_command(ctx):
    # Получаем статистику из сессии
    first_start = ctx.get_session_value('first_start', 'никогда')
    starts_count = ctx.get_session_value('starts_count', 0)
    messages_count = ctx.get_session_value('messages_count', 0)
    
    await ctx.reply(
        f"Статистика использования бота:\n"
        f"- Первый запуск: {first_start}\n"
        f"- Количество запусков: {starts_count}\n"
        f"- Отправлено сообщений: {messages_count}"
    )

# Обработчик команды /reset
@bot.command("reset")
async def reset_command(ctx):
    ctx.clear_session()
    await ctx.reply("Ваша сессия сброшена.")

# Обработчик всех текстовых сообщений
@bot.on("message_created")
async def message_handler(ctx):
    if ctx.message and hasattr(ctx.message.body, "text") and ctx.message.body.text:
        # Игнорируем команды (сообщения, начинающиеся с /)
        if not ctx.message.body.text.startswith('/'):
            # Увеличиваем счетчик сообщений
            messages_count = ctx.increment_counter('messages_count')
            
            await ctx.reply(
                f"Вы отправили: {ctx.message.body.text}\n"
                f"Это ваше {messages_count}-е сообщение."
            )

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