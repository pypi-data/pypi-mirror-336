# Интерактивные клавиатуры

Maxgram позволяет создавать интерактивные клавиатуры, которые помогают пользователям взаимодействовать с ботом. Клавиатуры отображаются под сообщениями и могут содержать различные типы кнопок.

## Типы кнопок

В Maxgram есть несколько типов кнопок:

- **Callback** - кнопка, при нажатии на которую отправляется callback-запрос
- **Link** - кнопка-ссылка, которая открывает указанный URL
- **Request GeoLocation** - кнопка для запроса геолокации пользователя
- **Request Contact** - кнопка для запроса контактной информации пользователя
- **Chat** - кнопка для создания нового чата

## Создание inline-клавиатуры

Для создания клавиатуры используйте модуль `keyboard`:

```python
from maxgram import Bot
from maxgram.core.helpers.keyboard import button, inline_keyboard

bot = Bot("YOUR_BOT_TOKEN")

@bot.command("menu")
async def menu_command(ctx):
    # Создаем клавиатуру с двумя рядами кнопок
    keyboard = inline_keyboard([
        # Первый ряд с двумя кнопками
        [
            button.callback("Кнопка 1", "button1"),
            button.callback("Кнопка 2", "button2")
        ],
        # Второй ряд с одной кнопкой
        [
            button.link("Посетить сайт", "https://example.com")
        ]
    ])
    
    await ctx.reply("Выберите действие:", {
        "attachments": [keyboard.to_dict()]
    })
```

## Обработка нажатий на кнопки

Когда пользователь нажимает на кнопку, генерируется событие `message_callback`. Вы можете обрабатывать это событие с помощью метода `action`:

```python
@bot.action("button1")
async def button1_handler(ctx):
    await ctx.answer_on_callback({
        "notification": "Вы нажали на кнопку 1"
    })

@bot.action("button2")
async def button2_handler(ctx):
    await ctx.answer_on_callback({
        "notification": "Вы нажали на кнопку 2"
    })
```

## Изменение сообщения после нажатия на кнопку

Вы можете изменить текст сообщения и/или клавиатуру после нажатия на кнопку:

```python
@bot.action("change_message")
async def change_message_handler(ctx):
    await ctx.answer_on_callback({
        "message": {
            "text": "Сообщение изменено!",
            "attachments": []  # Убираем клавиатуру
        }
    })
```

## Кнопки с разными цветами

Вы можете изменять внешний вид кнопок с помощью свойства `intent`:

```python
keyboard = inline_keyboard([
    [
        button.callback("По умолчанию", "default"),
        button.callback("Позитивная", "positive", {"intent": "positive"}),
        button.callback("Негативная", "negative", {"intent": "negative"})
    ]
])
```

## Запрос геолокации

Для запроса геолокации используйте кнопку `request_geo_location`:

```python
@bot.command("location")
async def location_command(ctx):
    keyboard = inline_keyboard([
        [
            button.request_geo_location("Отправить моё местоположение")
        ]
    ])
    
    await ctx.reply("Для продолжения, пожалуйста, поделитесь вашим местоположением:", {
        "attachments": [keyboard.to_dict()]
    })
```

Когда пользователь отправляет геолокацию, вы можете получить её через свойство `ctx.location`:

```python
@bot.on("message_created")
async def location_handler(ctx):
    if ctx.location:
        await ctx.reply(f"Спасибо! Ваши координаты: {ctx.location['latitude']}, {ctx.location['longitude']}")
```

## Запрос контактной информации

Для запроса контактной информации используйте кнопку `request_contact`:

```python
@bot.command("contact")
async def contact_command(ctx):
    keyboard = inline_keyboard([
        [
            button.request_contact("Поделиться контактом")
        ]
    ])
    
    await ctx.reply("Для продолжения, пожалуйста, поделитесь вашим контактом:", {
        "attachments": [keyboard.to_dict()]
    })
```

Когда пользователь отправляет контакт, вы можете получить его через свойство `ctx.contact_info`:

```python
@bot.on("message_created")
async def contact_handler(ctx):
    if ctx.contact_info:
        name = ctx.contact_info.get('fullName', 'Не указано')
        phone = ctx.contact_info.get('tel', 'Не указано')
        await ctx.reply(f"Спасибо! Ваше имя: {name}, телефон: {phone}")
```

## Создание нового чата

Для создания нового чата используйте кнопку `chat`:

```python
@bot.command("create_chat")
async def create_chat_command(ctx):
    keyboard = inline_keyboard([
        [
            button.chat("Создать чат", "Новый чат")
        ]
    ])
    
    await ctx.reply("Нажмите на кнопку ниже, чтобы создать новый чат:", {
        "attachments": [keyboard.to_dict()]
    })
```

## Пример комплексной клавиатуры

Вот пример более сложной клавиатуры, объединяющей различные типы кнопок:

```python
@bot.command("complex")
async def complex_keyboard_command(ctx):
    keyboard = inline_keyboard([
        [
            button.callback("Действие 1", "action1"),
            button.callback("Действие 2", "action2", {"intent": "positive"})
        ],
        [
            button.link("Документация", "https://dev.max.ru/")
        ],
        [
            button.request_geo_location("Отправить местоположение")
        ],
        [
            button.request_contact("Отправить контакт")
        ],
        [
            button.callback("Отмена", "cancel", {"intent": "negative"})
        ]
    ])
    
    await ctx.reply("Выберите действие:", {
        "attachments": [keyboard.to_dict()]
    })
```

## Следующие шаги

Теперь вы знаете, как создавать интерактивные клавиатуры и обрабатывать нажатия на кнопки. Далее вы можете:

- [Узнать, как настраивать контекст под свои нужды](./05-custom-context.md) 