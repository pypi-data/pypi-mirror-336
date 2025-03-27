# Maxgram: Python API Client для Max Messenger

Это не официальная открытая библиотека для поддержки Python при создании бота в мессенджере Max

## Документация

В [документации](./docs) вы можете найти подробные инструкции по использованию.

## Быстрый старт

> Если вы новичок, то можете прочитать [официальную документацию](https://dev.max.ru/), написанную разработчиками Max

### Получение токена
Откройте диалог с [MasterBot](https://max.ru/masterbot), следуйте инструкциям и создайте нового бота. После создания бота MasterBot отправит вам токен.

### Установка
```bash
pip install maxgram
```

### Пример
```python
from maxgram import Bot

# Создание экземпляра бота
bot = Bot("YOUR_BOT_TOKEN")

# Установка подсказок с доступными командами
bot.api.set_my_commands([
    {
        "name": "ping",
        "description": "Сыграть в пинг-понг"
    },
])

# Обработчик события запуска бота
@bot.on("bot_started")
async def on_bot_started(ctx):
    await ctx.reply("Привет! Отправь мне команду /ping, чтобы сыграть в пинг-понг")

# Обработчик команды '/ping'
@bot.command("ping")
async def ping_command(ctx):
    await ctx.reply("pong")

# Обработчик для сообщения с текстом 'hello'
@bot.hears("hello")
async def hello_handler(ctx):
    await ctx.reply("world")

# Обработчик для всех остальных входящих сообщений
@bot.on("message_created")
async def echo(ctx):
    await ctx.reply(ctx.message.body.text)

# Запуск бота
bot.start()
```

### Обработка ошибок
Если во время обработки события произойдёт ошибка, Bot вызовет метод `bot.handle_error`. По умолчанию `bot.handle_error` просто завершает работу программы, но вы можете переопределить это поведение, используя `bot.catch`.

> ⚠️ Завершайте работу программы при неизвестных ошибках, иначе бот может зависнуть в состоянии ошибки.

> ℹ️ [`pm2`](https://pm2.keymetrics.io/) может автоматически перезапустить вашего бота, если он остановится по какой-либо причине

```python
@bot.catch
async def handle_error(err, ctx):
    # Обработка ошибки
    print(f"Ошибка: {err}")
    # Вы можете решить, нужно ли завершать работу программы
    # или продолжить выполнение
```

## Лицензия
MIT 