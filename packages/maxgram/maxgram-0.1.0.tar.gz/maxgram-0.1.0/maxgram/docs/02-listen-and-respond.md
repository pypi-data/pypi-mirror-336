# Обработка событий и ответы

В Maxgram существует несколько типов событий, которые ваш бот может обрабатывать. В этом разделе мы рассмотрим, как слушать эти события и отвечать на них.

## Типы событий

Наиболее распространенные типы событий:

- `bot_started` — пользователь запустил бота
- `message_created` — пользователь отправил сообщение
- `message_callback` — пользователь нажал на кнопку в сообщении
- `message_edited` — сообщение было отредактировано
- `message_deleted` — сообщение было удалено

## Обработка запуска бота

Когда пользователь впервые запускает вашего бота, генерируется событие `bot_started`. Вы можете обработать его так:

```python
@bot.on("bot_started")
async def on_bot_started(ctx):
    await ctx.reply("Привет! Я ваш бот. Используйте команду /help, чтобы узнать, что я умею.")
```

## Обработка команд

Команды — это сообщения, начинающиеся с символа `/`. Вы можете обрабатывать команды с помощью метода `command`:

```python
@bot.command("start")
async def start_command(ctx):
    await ctx.reply("Привет! Добро пожаловать в бота.")

@bot.command("help")
async def help_command(ctx):
    await ctx.reply("Вот список доступных команд:\n/start - Запуск бота\n/help - Показать эту справку")
```

Вы также можете использовать регулярные выражения для более сложных команд:

```python
@bot.command(/echo\s+(.+)/)
async def echo_command(ctx):
    # ctx.match содержит результат регулярного выражения
    text_to_echo = ctx.match.group(1) if ctx.match else "Нечего повторить"
    await ctx.reply(text_to_echo)
```

## Обработка текстовых сообщений

Метод `hears` позволяет реагировать на конкретные текстовые сообщения:

```python
@bot.hears("привет")
async def hello_handler(ctx):
    await ctx.reply("И тебе привет!")

# Вы также можете использовать регулярные выражения
@bot.hears(/как (дела|настроение)/)
async def how_are_you_handler(ctx):
    await ctx.reply("У меня всё отлично, спасибо что спросили!")
```

## Обработка всех сообщений

Если вы хотите обрабатывать все входящие сообщения, используйте событие `message_created`:

```python
@bot.on("message_created")
async def all_messages_handler(ctx):
    print(f"Получено сообщение: {ctx.message.body.text}")
    # Обрабатывайте сообщение здесь
```

## Обработка callback-кнопок

Когда пользователь нажимает на интерактивную кнопку, генерируется событие `message_callback`:

```python
@bot.action("button_clicked")
async def button_handler(ctx):
    await ctx.answer_on_callback({
        "notification": "Вы нажали на кнопку!"
    })
    
    # Вы также можете изменить сообщение
    await ctx.answer_on_callback({
        "message": {
            "text": "Сообщение изменено после нажатия на кнопку",
            "attachments": []
        }
    })
```

Вы также можете использовать регулярные выражения для обработки разных payload:

```python
@bot.action(/button_(\d+)/)
async def button_with_id_handler(ctx):
    button_id = ctx.match.group(1) if ctx.match else "unknown"
    await ctx.answer_on_callback({
        "notification": f"Вы нажали на кнопку {button_id}"
    })
```

## Приоритет обработчиков

Обработчики выполняются в порядке их регистрации. Если несколько обработчиков подходят для одного события, будет выполнен первый зарегистрированный обработчик, который соответствует условиям.

Обычно рекомендуется регистрировать более специфичные обработчики перед более общими:

```python
# Сначала специфичные обработчики
@bot.command("start")
async def start_command(ctx):
    await ctx.reply("Запуск бота")

@bot.hears("привет")
async def hello_handler(ctx):
    await ctx.reply("И тебе привет!")

# Затем более общие обработчики
@bot.on("message_created")
async def all_messages_handler(ctx):
    # Этот обработчик выполнится только если предыдущие не сработали
    await ctx.reply("Я не понимаю, что вы хотите.")
```

## Использование Middleware

Middleware позволяет обрабатывать сообщения до того, как они попадут в обработчики. Это полезно для логирования, проверки прав доступа и т.д.

```python
async def logging_middleware(ctx, next):
    print(f"Обработка события {ctx.update.update_type}")
    
    # Вызываем следующий middleware или обработчик
    await next()
    
    print(f"Событие {ctx.update.update_type} обработано")

# Регистрация middleware
bot.use(logging_middleware)
```

Middleware можно комбинировать для создания сложной логики обработки событий.

## Ответ на сообщения

В контексте (`ctx`) доступны различные методы для ответа на сообщения:

### Простой ответ

```python
await ctx.reply("Текстовый ответ")
```

### Ответ с дополнительными параметрами

```python
await ctx.reply("Ответ на сообщение", {
    "reply_to_message_id": ctx.message.id  # Ответ на конкретное сообщение
})
```

### Пересылка сообщения

```python
# Пересылка сообщения в другой чат
new_message = await ctx.forward(other_chat_id)
```

### Удаление сообщения

```python
result = await ctx.delete_message()
```

## Следующие шаги

Теперь, когда вы знаете, как обрабатывать события и отвечать на них, вы можете:

- [Узнать о работе с вложениями и файлами](./03-attachments.md)
- [Изучить создание интерактивных клавиатур](./04-keyboard.md)
- [Настроить контекст под свои нужды](./05-custom-context.md) 