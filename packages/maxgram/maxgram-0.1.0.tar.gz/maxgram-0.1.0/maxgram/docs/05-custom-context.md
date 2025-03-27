# Пользовательский контекст

По умолчанию все обработчики событий получают объект контекста типа `Context`. Однако, если вам нужно добавить собственную логику или дополнительные свойства, вы можете создать свой класс контекста.

## Создание пользовательского контекста

Чтобы создать свой контекст, унаследуйте класс от базового `Context`:

```python
from maxgram import Bot, Context

class CustomContext(Context):
    """
    Пользовательский контекст с дополнительными возможностями
    """
    
    def __init__(self, update, api, bot_info=None):
        super().__init__(update, api, bot_info)
        # Дополнительные свойства
        self.session = {}
    
    # Новые методы
    async def reply_with_greeting(self, name):
        await self.reply(f"Привет, {name}!")
    
    async def log_message(self):
        if self.message:
            print(f"Сообщение от {self.message.from_user.get('first_name')}: {self.message.body.text}")
```

## Использование пользовательского контекста

Чтобы использовать свой контекст, передайте его при создании объекта бота:

```python
from maxgram import Bot
from maxgram.bot import BotConfig

# Создание конфигурации с пользовательским контекстом
config = BotConfig(context_type=CustomContext)

# Создание бота с этой конфигурацией
bot = Bot("YOUR_BOT_TOKEN", config)

# Теперь во всех обработчиках будет использоваться ваш контекст
@bot.command("start")
async def start_command(ctx):
    # ctx - это экземпляр CustomContext
    await ctx.reply_with_greeting("Пользователь")
    await ctx.log_message()
```

## Добавление пользовательских данных сессии

Один из распространенных случаев использования пользовательского контекста — хранение данных сессии:

```python
import json
from typing import Dict
from maxgram import Bot, Context

# Глобальное хранилище данных пользователей
session_storage: Dict[int, Dict] = {}

class SessionContext(Context):
    """
    Контекст с поддержкой сессий пользователей
    """
    
    def __init__(self, update, api, bot_info=None):
        super().__init__(update, api, bot_info)
        
        # Инициализация сессии пользователя
        self.user_id = None
        if self.message and hasattr(self.message, 'from_user'):
            self.user_id = self.message.from_user.get('id')
        elif self.update.update_type == 'message_callback' and hasattr(self.update.callback, 'from_user'):
            self.user_id = self.update.callback.from_user.get('id')
            
        if self.user_id:
            if self.user_id not in session_storage:
                session_storage[self.user_id] = {}
            self.session = session_storage[self.user_id]
        else:
            self.session = {}
    
    def set_session_data(self, key, value):
        """
        Сохраняет данные в сессии
        """
        if self.user_id:
            self.session[key] = value
            return True
        return False
    
    def get_session_data(self, key, default=None):
        """
        Извлекает данные из сессии
        """
        return self.session.get(key, default)
    
    def clear_session(self):
        """
        Очищает сессию пользователя
        """
        if self.user_id and self.user_id in session_storage:
            session_storage[self.user_id] = {}
            self.session = {}
            return True
        return False
```

## Пример использования контекста с сессией

```python
from maxgram import Bot
from maxgram.bot import BotConfig

# Используем созданный выше SessionContext
config = BotConfig(context_type=SessionContext)
bot = Bot("YOUR_BOT_TOKEN", config)

@bot.command("start")
async def start_command(ctx):
    # Сохраняем информацию о запуске бота
    ctx.set_session_data('started', True)
    ctx.set_session_data('start_time', ctx.update.timestamp)
    
    await ctx.reply("Привет! Я запомнил, что вы запустили меня.")

@bot.command("status")
async def status_command(ctx):
    # Проверяем, запускал ли пользователь бота
    started = ctx.get_session_data('started', False)
    start_time = ctx.get_session_data('start_time')
    
    if started:
        await ctx.reply(f"Вы запустили бота в {start_time}")
    else:
        await ctx.reply("Вы еще не использовали команду /start")

@bot.command("reset")
async def reset_command(ctx):
    # Очищаем сессию
    ctx.clear_session()
    await ctx.reply("Ваша сессия сброшена")
```

## Сохранение данных сессии между перезапусками

В реальном приложении вы можете захотеть сохранять данные сессии между перезапусками бота. Для этого можно использовать базу данных, Redis или даже простой JSON-файл:

```python
import json
import os
from maxgram import Bot, Context

# Загрузка данных сессии из файла
session_file = 'sessions.json'
session_storage = {}

if os.path.exists(session_file):
    try:
        with open(session_file, 'r') as f:
            session_storage = json.load(f)
    except json.JSONDecodeError:
        session_storage = {}

class PersistentSessionContext(Context):
    # ... (такой же код, как в SessionContext) ...
    
    @staticmethod
    def save_all_sessions():
        """
        Сохраняет все сессии в файл
        """
        with open(session_file, 'w') as f:
            json.dump(session_storage, f)

# Сохраняем сессии при выходе
import atexit
atexit.register(PersistentSessionContext.save_all_sessions)
```

## Заключение

Пользовательский контекст — это мощный инструмент, который позволяет расширить возможности вашего бота и добавить дополнительную логику обработки событий.

Вы можете:
- Добавлять новые методы для удобства разработки
- Хранить информацию о сессиях пользователей
- Интегрироваться с базами данных или внешними API
- Создавать более сложную логику обработки сообщений

Это завершает основную документацию по использованию Max Bot API. Теперь вы знаете все основные возможности библиотеки и можете создавать свои собственные боты! 