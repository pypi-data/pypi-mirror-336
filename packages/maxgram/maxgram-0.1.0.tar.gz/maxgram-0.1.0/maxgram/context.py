from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import re

from .core.helpers.types import Guard, MaybeArray
from .core.network.api import (
    Api, BotInfo, Message, SendMessageExtra, Update, UpdateType
)
from .core.helpers.attachments import (
    LocationAttachment, ShareAttachment
)

T = TypeVar('T', bound=Update)

class FilteredContext(Generic[T]):
    """
    Тип для контекста с примененным фильтром
    """
    pass

class Context:
    """
    Контекст для обработки событий
    """
    
    def __init__(self, update: Update, api: Api, bot_info: Optional[BotInfo] = None):
        self.update = update
        self.api = api
        self.bot_info = bot_info
        self.match: Optional[re.Match] = None
        self._message: Optional[Message] = None
        self._location: Optional[Dict[str, float]] = None
        self._contact_info: Optional[Dict[str, Any]] = None
    
    @property
    def my_id(self) -> Optional[int]:
        """
        ID бота
        """
        if self.bot_info:
            return self.bot_info.id
        return None
    
    @property
    def message(self) -> Optional[Message]:
        """
        Сообщение из обновления
        """
        if self._message:
            return self._message
        
        if self.update.update_type == 'message_created':
            self._message = self.update.message
        elif self.update.update_type == 'message_callback':
            self._message = self.update.message
            
        return self._message
    
    @property
    def location(self) -> Optional[Dict[str, float]]:
        """
        Геолокация из сообщения
        """
        if self._location:
            return self._location
            
        if not self.message or not self.message.body:
            return None
            
        if not hasattr(self.message.body, 'attachments'):
            return None
            
        for attachment in self.message.body.attachments:
            if isinstance(attachment, LocationAttachment):
                self._location = {
                    'latitude': attachment.latitude,
                    'longitude': attachment.longitude
                }
                return self._location
                
        return None
    
    @property
    def contact_info(self) -> Optional[Dict[str, Any]]:
        """
        Контактная информация из сообщения
        """
        if self._contact_info:
            return self._contact_info
            
        if not self.message or not self.message.body:
            return None
            
        if not hasattr(self.message.body, 'attachments'):
            return None
            
        for attachment in self.message.body.attachments:
            if isinstance(attachment, ShareAttachment) and attachment.type == 'contact':
                self._contact_info = attachment.contact
                return self._contact_info
                
        return None
    
    async def reply(self, text: str, extra: Optional[SendMessageExtra] = None) -> Message:
        """
        Отправляет ответное сообщение
        """
        if not self.message:
            raise RuntimeError('Unable to reply: no source message in context')
            
        chat_id = self.message.chat.id
        
        extra_params = extra or {}
        result = await self.api.send_message_to_chat(chat_id, text, extra_params)
        return result
        
    async def forward(self, chat_id: int) -> Message:
        """
        Пересылает сообщение другому пользователю или в другой чат
        """
        if not self.message:
            raise RuntimeError('Unable to forward: no source message in context')
            
        result = await self.api.send_message_to_chat(
            chat_id, 
            self.message.body.text or '', 
            {'forward_from_message_id': self.message.id}
        )
        return result
    
    async def delete_message(self) -> Dict[str, Any]:
        """
        Удаляет сообщение
        """
        if not self.message:
            raise RuntimeError('Unable to delete: no source message in context')
            
        return await self.api.delete_message(self.message.id)
    
    async def answer_on_callback(self, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Отвечает на callback запрос
        """
        if self.update.update_type != 'message_callback':
            raise RuntimeError('Unable to answer on callback: not a callback update')
            
        callback_id = self.update.callback.id
        extra = extra or {}
        
        return await self.api.answer_on_callback(callback_id, extra)
    
    def has(self, filters: MaybeArray[Union[UpdateType, Guard]]) -> bool:
        """
        Проверяет, соответствует ли контекст указанному типу или фильтру
        """
        if not filters:
            return False
            
        if not isinstance(filters, list):
            filters = [filters]
            
        for filter_item in filters:
            if isinstance(filter_item, str):
                if self.update.update_type == filter_item:
                    return True
            elif callable(filter_item) and filter_item(self.update):
                return True
                
        return False 