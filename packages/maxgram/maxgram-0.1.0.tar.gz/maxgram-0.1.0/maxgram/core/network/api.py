import json
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

import aiohttp
import logging

logger = logging.getLogger('maxbot-api')

# Типы обновлений
UpdateType = Literal[
    'bot_started',
    'message_created',
    'message_callback',
    'message_edited',
    'message_deleted',
    'chat_title_changed',
    'chat_photo_changed',
    'chat_members_updated',
    'pinned_message_changed'
]

# Действия отправителя
SenderAction = Literal[
    'typing',
    'upload_photo',
    'upload_video',
    'upload_audio',
    'upload_document'
]

# Типизированные данные
class ClientOptions(TypedDict, total=False):
    """
    Опции для клиента API
    """
    base_url: str
    headers: Dict[str, str]

class BotInfo(TypedDict):
    """
    Информация о боте
    """
    id: int
    username: str
    first_name: str
    last_name: Optional[str]
    avatar_url: Optional[str]
    is_bot: bool

class BotCommand(TypedDict):
    """
    Команда бота
    """
    name: str
    description: str

class GetUpdatesDTO(TypedDict, total=False):
    """
    Параметры для получения обновлений
    """
    limit: int
    timeout: int
    offset: str
    types: str

class EditMyInfoDTO(TypedDict, total=False):
    """
    Параметры для редактирования информации о боте
    """
    first_name: str
    last_name: str
    commands: List[BotCommand]

class SendMessageExtra(TypedDict, total=False):
    """
    Дополнительные параметры для отправки сообщений
    """
    reply_to_message_id: str
    forward_from_message_id: str
    attachments: List[Dict[str, Any]]

class EditMessageExtra(TypedDict, total=False):
    """
    Дополнительные параметры для редактирования сообщений
    """
    text: str
    attachments: List[Dict[str, Any]]

class DeleteMessageExtra(TypedDict, total=False):
    """
    Дополнительные параметры для удаления сообщений
    """
    for_all: bool

class AnswerOnCallbackExtra(TypedDict, total=False):
    """
    Дополнительные параметры для ответа на callback
    """
    notification: str
    message: Dict[str, Any]

class GetMessagesExtra(TypedDict, total=False):
    """
    Дополнительные параметры для получения сообщений
    """
    message_ids: List[str]
    limit: int
    offset: int

class GetAllChatsExtra(TypedDict, total=False):
    """
    Дополнительные параметры для получения всех чатов
    """
    limit: int
    offset: int

class EditChatExtra(TypedDict, total=False):
    """
    Дополнительные параметры для редактирования чата
    """
    title: str
    photo: Dict[str, Any]

class GetChatMembersExtra(TypedDict, total=False):
    """
    Дополнительные параметры для получения участников чата
    """
    user_ids: List[int]
    limit: int
    offset: int

class PinMessageExtra(TypedDict, total=False):
    """
    Дополнительные параметры для закрепления сообщения
    """
    notify: bool

# Вспомогательный тип для уплощения вложенных словарей
FlattenReq = Dict[str, Any]

class Chat(TypedDict):
    """
    Информация о чате
    """
    id: int
    title: str
    type: str

class MessageBody(TypedDict):
    """
    Тело сообщения
    """
    text: str
    markup: Optional[List[Dict[str, Any]]]
    attachments: Optional[List[Dict[str, Any]]]

class Message(TypedDict):
    """
    Сообщение
    """
    id: str
    chat: Chat
    from_user: Dict[str, Any]
    body: MessageBody
    created_at: int
    updated_at: int

class Callback(TypedDict):
    """
    Информация о callback
    """
    id: str
    from_user: Dict[str, Any]
    payload: str

class Update(TypedDict):
    """
    Обновление
    """
    timestamp: int
    update_type: UpdateType
    message: Optional[Message]
    callback: Optional[Callback]

class MaxError(Exception):
    """
    Ошибка API Max
    """
    def __init__(self, message: str, code: int = 0):
        self.code = code
        super().__init__(message)

class Client:
    """
    Клиент для работы с API Max
    """
    
    def __init__(self, token: str, options: Optional[ClientOptions] = None):
        self.token = token
        options = options or {}
        
        self.base_url = options.get('base_url', 'https://api.max.ru/v1')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            **options.get('headers', {})
        }
    
    async def request(self, method: str, path: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Выполняет запрос к API
        """
        url = f"{self.base_url}{path}"
        data = data or {}
        
        logger.debug(f"API Request: {method} {path}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data if method.lower() != 'get' else None,
                    params=data if method.lower() == 'get' else None
                ) as response:
                    result = await response.json()
                    
                    if not response.ok:
                        error_message = result.get('message', 'Unknown API error')
                        error_code = result.get('code', 0)
                        raise MaxError(error_message, error_code)
                    
                    return result
            except aiohttp.ClientError as e:
                raise MaxError(f"HTTP Error: {str(e)}")

def create_client(token: str, options: Optional[ClientOptions] = None) -> Client:
    """
    Создает клиент для работы с API
    """
    return Client(token, options)

# Модули API
class BotsModule:
    """
    Модуль для работы с ботами
    """
    
    def __init__(self, client: Client):
        self.client = client
    
    async def get_my_info(self) -> BotInfo:
        """
        Получает информацию о текущем боте
        """
        result = await self.client.request('GET', '/bots/me')
        return result.get('bot', {})
    
    async def edit_my_info(self, data: FlattenReq[EditMyInfoDTO]) -> Dict[str, Any]:
        """
        Редактирует информацию о боте
        """
        return await self.client.request('PATCH', '/bots/me', data)

class ChatsModule:
    """
    Модуль для работы с чатами
    """
    
    def __init__(self, client: Client):
        self.client = client
    
    async def get_all(self, data: FlattenReq[GetAllChatsExtra]) -> Dict[str, Any]:
        """
        Получает список всех чатов
        """
        return await self.client.request('GET', '/chats', data)
    
    async def get_by_id(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает чат по ID
        """
        return await self.client.request('GET', '/chats/getById', data)
    
    async def get_by_link(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает чат по ссылке
        """
        return await self.client.request('GET', '/chats/getByLink', data)
    
    async def edit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Редактирует информацию о чате
        """
        return await self.client.request('PATCH', '/chats/edit', data)
    
    async def get_chat_membership(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает информацию о членстве в чате
        """
        return await self.client.request('GET', '/chats/getChatMembership', data)
    
    async def get_chat_admins(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает список администраторов чата
        """
        return await self.client.request('GET', '/chats/getChatAdmins', data)
    
    async def add_chat_members(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Добавляет пользователей в чат
        """
        return await self.client.request('POST', '/chats/addChatMembers', data)
    
    async def get_chat_members(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает список участников чата
        """
        return await self.client.request('GET', '/chats/getChatMembers', data)
    
    async def remove_chat_member(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Удаляет участника из чата
        """
        return await self.client.request('POST', '/chats/removeChatMember', data)
    
    async def get_pinned_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает закрепленное сообщение
        """
        return await self.client.request('GET', '/chats/getPinnedMessage', data)
    
    async def pin_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Закрепляет сообщение
        """
        return await self.client.request('POST', '/chats/pinMessage', data)
    
    async def unpin_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Открепляет сообщение
        """
        return await self.client.request('POST', '/chats/unpinMessage', data)
    
    async def send_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет действие (статус набора текста и т.п.)
        """
        return await self.client.request('POST', '/chats/sendAction', data)
    
    async def leave_chat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выходит из чата
        """
        return await self.client.request('POST', '/chats/leaveChat', data)

class MessagesModule:
    """
    Модуль для работы с сообщениями
    """
    
    def __init__(self, client: Client):
        self.client = client
    
    async def send(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет сообщение
        """
        return await self.client.request('POST', '/messages/send', data)
    
    async def get(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает сообщения
        """
        return await self.client.request('GET', '/messages/get', data)
    
    async def get_by_id(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает сообщение по ID
        """
        return await self.client.request('GET', '/messages/getById', data)
    
    async def edit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Редактирует сообщение
        """
        return await self.client.request('PATCH', '/messages/edit', data)
    
    async def delete(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Удаляет сообщение
        """
        return await self.client.request('DELETE', '/messages/delete', data)
    
    async def answer_on_callback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отвечает на callback запрос
        """
        return await self.client.request('POST', '/messages/answerOnCallback', data)

class FilesModule:
    """
    Модуль для работы с файлами
    """
    
    def __init__(self, client: Client):
        self.client = client
    
    async def get_upload_url(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает URL для загрузки файла
        """
        return await self.client.request('GET', '/files/getUploadUrl', data)
    
    async def upload_by_url(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Загружает файл по ссылке
        """
        return await self.client.request('POST', '/files/uploadByUrl', data)

class SubscriptionsModule:
    """
    Модуль для работы с подписками
    """
    
    def __init__(self, client: Client):
        self.client = client
    
    async def get_updates(self, data: FlattenReq[GetUpdatesDTO]) -> Dict[str, Any]:
        """
        Получает обновления
        """
        return await self.client.request('GET', '/subscriptions/getUpdates', data)

class RawApi:
    """
    Низкоуровневый API для доступа к модулям
    """
    
    def __init__(self, client: Client):
        self.client = client
        self.bots = BotsModule(client)
        self.chats = ChatsModule(client)
        self.messages = MessagesModule(client)
        self.files = FilesModule(client)
        self.subscriptions = SubscriptionsModule(client) 