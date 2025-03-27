# Работа с вложениями

В Max Bot API поддерживается несколько типов вложений, которые можно отправлять в сообщениях:

- Изображения
- Видео
- Аудио
- Файлы
- Стикеры
- Геолокация
- Контакты

## Отправка изображений

Библиотека предоставляет несколько способов отправки изображений:

### Загрузка изображения по пути

```python
from maxbot_api import Bot

bot = Bot("YOUR_BOT_TOKEN")

@bot.command("photo")
async def photo_command(ctx):
    # Загрузка из локального файла
    image = await bot.api.upload_image({
        "path": "path/to/image.jpg"
    })
    
    await ctx.reply("Вот ваша фотография:", {
        "attachments": [image]
    })
```

### Загрузка изображения по URL

```python
@bot.command("cat")
async def cat_command(ctx):
    # Загрузка по URL
    image = await bot.api.upload_image({
        "url": "https://example.com/cat.jpg"
    })
    
    await ctx.reply("Вот случайная фотография кота:", {
        "attachments": [image]
    })
```

## Отправка видео

```python
@bot.command("video")
async def video_command(ctx):
    # Загрузка из локального файла
    video = await bot.api.upload_video({
        "path": "path/to/video.mp4",
        "width": 1280,
        "height": 720,
        "duration": 30  # в секундах
    })
    
    await ctx.reply("Вот ваше видео:", {
        "attachments": [video]
    })
```

## Отправка аудио

```python
@bot.command("audio")
async def audio_command(ctx):
    # Загрузка из локального файла
    audio = await bot.api.upload_audio({
        "path": "path/to/audio.mp3",
        "duration": 180,  # в секундах
        "title": "Название трека",
        "performer": "Исполнитель"
    })
    
    await ctx.reply("Вот ваше аудио:", {
        "attachments": [audio]
    })
```

## Отправка файлов

```python
@bot.command("file")
async def file_command(ctx):
    # Загрузка из локального файла
    file = await bot.api.upload_file({
        "path": "path/to/document.pdf",
        "filename": "document.pdf"
    })
    
    await ctx.reply("Вот ваш документ:", {
        "attachments": [file]
    })
```

## Отправка стикеров

```python
from maxbot_api import StickerAttachment

@bot.command("sticker")
async def sticker_command(ctx):
    sticker = StickerAttachment("sticker_id", "😊")
    
    await ctx.reply("Вот стикер:", {
        "attachments": [sticker]
    })
```

## Отправка геолокации

```python
from maxbot_api import LocationAttachment

@bot.command("location")
async def location_command(ctx):
    location = LocationAttachment(55.753215, 37.622504)  # Москва
    
    await ctx.reply("Вот геолокация:", {
        "attachments": [location]
    })
```

## Отправка нескольких вложений

Вы можете отправлять несколько вложений в одном сообщении:

```python
@bot.command("gallery")
async def gallery_command(ctx):
    image1 = await bot.api.upload_image({
        "path": "path/to/image1.jpg"
    })
    
    image2 = await bot.api.upload_image({
        "path": "path/to/image2.jpg"
    })
    
    await ctx.reply("Галерея изображений:", {
        "attachments": [image1, image2]
    })
```

## Получение вложений

Когда пользователь отправляет вам вложение, вы можете получить его из контекста. Вложения находятся в `ctx.message.body.attachments`.

```python
@bot.on("message_created")
async def handle_attachments(ctx):
    if hasattr(ctx.message.body, "attachments") and ctx.message.body.attachments:
        attachments = ctx.message.body.attachments
        
        # Проверяем первое вложение
        first_attachment = attachments[0]
        
        if first_attachment.type == "image":
            await ctx.reply(f"Вы отправили изображение размером {first_attachment.width}x{first_attachment.height} пикселей")
        
        elif first_attachment.type == "video":
            await ctx.reply(f"Вы отправили видео длительностью {first_attachment.duration} секунд")
        
        elif first_attachment.type == "audio":
            await ctx.reply(f"Вы отправили аудио: {first_attachment.title} - {first_attachment.performer}")
        
        elif first_attachment.type == "file":
            await ctx.reply(f"Вы отправили файл: {first_attachment.filename} размером {first_attachment.size} байт")
        
        elif first_attachment.type == "location":
            await ctx.reply(f"Вы отправили геолокацию с координатами: {first_attachment.latitude}, {first_attachment.longitude}")
        
        else:
            await ctx.reply(f"Вы отправили вложение типа: {first_attachment.type}")
```

## Специальные хелперы для геолокации и контактов

В контексте (`ctx`) есть удобные свойства для работы с геолокацией и контактной информацией:

```python
@bot.on("message_created")
async def handle_location_and_contacts(ctx):
    # Проверяем наличие геолокации
    if ctx.location:
        await ctx.reply(f"Ваши координаты: {ctx.location['latitude']}, {ctx.location['longitude']}")
    
    # Проверяем наличие контактной информации
    if ctx.contact_info:
        name = ctx.contact_info.get('fullName', 'Не указано')
        phone = ctx.contact_info.get('tel', 'Не указано')
        await ctx.reply(f"Контактная информация:\nИмя: {name}\nТелефон: {phone}")
```

## Следующие шаги

Теперь вы знаете, как работать с вложениями. Далее вы можете:

- [Изучить создание интерактивных клавиатур](./04-keyboard.md)
- [Настроить контекст под свои нужды](./05-custom-context.md) 