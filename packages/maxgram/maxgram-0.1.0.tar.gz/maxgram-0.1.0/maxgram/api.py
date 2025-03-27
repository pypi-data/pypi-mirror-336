from typing import Dict, List, Optional, Any, Union

from .core.helpers.attachments import (
    AudioAttachment, FileAttachment, ImageAttachment, VideoAttachment
)
from .core.helpers.upload import Upload
from .core.helpers.types import MaybeArray

from .core.network.api import (
    RawApi, Client, GetMessagesExtra, SenderAction,
    AnswerOnCallbackExtra, SendMessageExtra, BotCommand, EditMessageExtra,
    DeleteMessageExtra, EditMyInfoDTO, FlattenReq, GetUpdatesDTO, UpdateType,
    EditChatExtra, GetAllChatsExtra, GetChatMembersExtra, PinMessageExtra
)

class MaxAPI:
    """
    Класс для взаимодействия с API Max
    """
    
    def __init__(self, client: Client):
        self.raw = RawApi(client)
        self.upload = Upload(self)
    
    async def get_my_info(self):
        """
        Получает информацию о боте
        """
        return await self.raw.bots.get_my_info()
    
    async def edit_my_info(self, extra: FlattenReq[EditMyInfoDTO]):
        """
        Изменяет информацию о боте
        """
        return await self.raw.bots.edit_my_info(extra)
    
    async def set_my_commands(self, commands: List[BotCommand]):
        """
        Устанавливает список команд бота
        """
        return await self.edit_my_info({'commands': commands})
    
    async def delete_my_commands(self):
        """
        Удаляет список команд бота
        """
        return await self.edit_my_info({'commands': []})
    
    async def get_all_chats(self, extra: GetAllChatsExtra = None):
        """
        Получает список всех чатов
        """
        extra = extra or {}
        return await self.raw.chats.get_all(extra)
    
    async def get_chat(self, id: int):
        """
        Получает информацию о чате по ID
        """
        return await self.raw.chats.get_by_id({'chat_id': id})
    
    async def get_chat_by_link(self, link: str):
        """
        Получает информацию о чате по ссылке
        """
        return await self.raw.chats.get_by_link({'chat_link': link})
    
    async def edit_chat_info(self, chat_id: int, extra: EditChatExtra):
        """
        Изменяет информацию о чате
        """
        return await self.raw.chats.edit({'chat_id': chat_id, **extra})
    
    async def send_message_to_chat(
        self, 
        chat_id: int, 
        text: str, 
        extra: Optional[SendMessageExtra] = None
    ):
        """
        Отправляет сообщение в чат
        """
        params = extra or {}
        result = await self.raw.messages.send({
            'chat_id': chat_id,
            'text': text,
            **params
        })
        return result['message']
    
    async def send_message_to_user(
        self, 
        user_id: int, 
        text: str, 
        extra: Optional[SendMessageExtra] = None
    ):
        """
        Отправляет сообщение пользователю
        """
        params = extra or {}
        result = await self.raw.messages.send({
            'user_id': user_id,
            'text': text,
            **params
        })
        return result['message']
    
    async def get_messages(self, chat_id: int, extra: Optional[GetMessagesExtra] = None):
        """
        Получает сообщения из чата
        """
        params = extra or {}
        message_ids = params.get('message_ids', [])
        
        # Удаляем message_ids из extra и добавляем строкой
        if 'message_ids' in params:
            del params['message_ids']
            
        joined_ids = None
        if message_ids:
            joined_ids = ','.join(str(mid) for mid in message_ids)
            
        return await self.raw.messages.get({
            'chat_id': chat_id,
            'message_ids': joined_ids,
            **params
        })
    
    async def get_message(self, id: str):
        """
        Получает сообщение по ID
        """
        return await self.raw.messages.get_by_id({'message_id': id})
    
    async def edit_message(self, message_id: str, extra: Optional[EditMessageExtra] = None):
        """
        Редактирует сообщение
        """
        params = extra or {}
        return await self.raw.messages.edit({
            'message_id': message_id,
            **params
        })
    
    async def delete_message(self, message_id: str, extra: Optional[DeleteMessageExtra] = None):
        """
        Удаляет сообщение
        """
        params = extra or {}
        return await self.raw.messages.delete({
            'message_id': message_id,
            **params
        })
    
    async def answer_on_callback(self, callback_id: str, extra: Optional[AnswerOnCallbackExtra] = None):
        """
        Отвечает на callback запрос
        """
        params = extra or {}
        return await self.raw.messages.answer_on_callback({
            'callback_id': callback_id,
            **params
        })
    
    async def get_chat_membership(self, chat_id: int):
        """
        Получает информацию о членстве в чате
        """
        return await self.raw.chats.get_chat_membership({'chat_id': chat_id})
    
    async def get_chat_admins(self, chat_id: int):
        """
        Получает список администраторов чата
        """
        return await self.raw.chats.get_chat_admins({'chat_id': chat_id})
    
    async def add_chat_members(self, chat_id: int, user_ids: List[int]):
        """
        Добавляет пользователей в чат
        """
        return await self.raw.chats.add_chat_members({
            'chat_id': chat_id,
            'user_ids': user_ids
        })
    
    async def get_chat_members(self, chat_id: int, extra: Optional[GetChatMembersExtra] = None):
        """
        Получает список участников чата
        """
        params = extra or {}
        user_ids = params.get('user_ids', [])
        
        # Удаляем user_ids из extra и добавляем строкой
        if 'user_ids' in params:
            del params['user_ids']
            
        joined_ids = None
        if user_ids:
            joined_ids = ','.join(str(uid) for uid in user_ids)
            
        return await self.raw.chats.get_chat_members({
            'chat_id': chat_id,
            'user_ids': joined_ids,
            **params
        })
    
    async def remove_chat_member(self, chat_id: int, user_id: int):
        """
        Удаляет участника из чата
        """
        return await self.raw.chats.remove_chat_member({
            'chat_id': chat_id,
            'user_id': user_id
        })
    
    async def get_updates(
        self, 
        types: MaybeArray[UpdateType] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        """
        Получает обновления с сервера
        """
        params = extra or {}
        update_types = types or []
        
        types_str = ''
        if update_types:
            if isinstance(update_types, list):
                types_str = ','.join(update_types)
            else:
                types_str = update_types
                
        return await self.raw.subscriptions.get_updates({
            'types': types_str,
            **params
        })
    
    async def get_pinned_message(self, chat_id: int):
        """
        Получает закрепленное сообщение
        """
        return await self.raw.chats.get_pinned_message({'chat_id': chat_id})
    
    async def pin_message(self, chat_id: int, message_id: str, extra: Optional[PinMessageExtra] = None):
        """
        Закрепляет сообщение
        """
        params = extra or {}
        return await self.raw.chats.pin_message({
            'chat_id': chat_id,
            'message_id': message_id,
            **params
        })
    
    async def unpin_message(self, chat_id: int):
        """
        Открепляет сообщение
        """
        return await self.raw.chats.unpin_message({'chat_id': chat_id})
    
    async def send_action(self, chat_id: int, action: SenderAction):
        """
        Отправляет действие (статус набора текста и т.п.)
        """
        return await self.raw.chats.send_action({
            'chat_id': chat_id,
            'action': action
        })
    
    async def leave_chat(self, chat_id: int):
        """
        Выходит из чата
        """
        return await self.raw.chats.leave_chat({'chat_id': chat_id})
    
    async def upload_image(self, options):
        """
        Загружает изображение
        """
        data = await self.upload.image(options)
        return ImageAttachment(data)
    
    async def upload_video(self, options):
        """
        Загружает видео
        """
        data = await self.upload.video(options)
        return VideoAttachment(data)
    
    async def upload_audio(self, options):
        """
        Загружает аудио
        """
        data = await self.upload.audio(options)
        return AudioAttachment(data)
    
    async def upload_file(self, options):
        """
        Загружает файл
        """
        data = await self.upload.file(options)
        return FileAttachment(data) 