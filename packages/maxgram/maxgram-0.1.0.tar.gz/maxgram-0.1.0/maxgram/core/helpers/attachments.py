from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class BaseAttachment:
    """
    Базовый класс для вложений
    """
    type: str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует вложение в словарь
        """
        return {'type': self.type}

@dataclass
class MediaAttachment(BaseAttachment):
    """
    Базовый класс для медиа-вложений
    """
    id: str
    url: str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует медиа-вложение в словарь
        """
        return {
            **super().to_dict(),
            'id': self.id,
            'url': self.url
        }

@dataclass
class ImageAttachment(MediaAttachment):
    """
    Вложение с изображением
    """
    width: int
    height: int
    thumbnail_url: Optional[str] = None
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(
            type='image',
            id=data.get('id', ''),
            url=data.get('url', '')
        )
        self.width = data.get('width', 0)
        self.height = data.get('height', 0)
        self.thumbnail_url = data.get('thumbnail_url')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует изображение в словарь
        """
        result = {
            **super().to_dict(),
            'width': self.width,
            'height': self.height
        }
        
        if self.thumbnail_url:
            result['thumbnail_url'] = self.thumbnail_url
            
        return result

@dataclass
class VideoAttachment(MediaAttachment):
    """
    Вложение с видео
    """
    width: int
    height: int
    duration: int
    thumbnail_url: Optional[str] = None
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(
            type='video',
            id=data.get('id', ''),
            url=data.get('url', '')
        )
        self.width = data.get('width', 0)
        self.height = data.get('height', 0)
        self.duration = data.get('duration', 0)
        self.thumbnail_url = data.get('thumbnail_url')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует видео в словарь
        """
        result = {
            **super().to_dict(),
            'width': self.width,
            'height': self.height,
            'duration': self.duration
        }
        
        if self.thumbnail_url:
            result['thumbnail_url'] = self.thumbnail_url
            
        return result

@dataclass
class AudioAttachment(MediaAttachment):
    """
    Вложение с аудио
    """
    duration: int
    title: Optional[str] = None
    performer: Optional[str] = None
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(
            type='audio',
            id=data.get('id', ''),
            url=data.get('url', '')
        )
        self.duration = data.get('duration', 0)
        self.title = data.get('title')
        self.performer = data.get('performer')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует аудио в словарь
        """
        result = {
            **super().to_dict(),
            'duration': self.duration
        }
        
        if self.title:
            result['title'] = self.title
        
        if self.performer:
            result['performer'] = self.performer
            
        return result

@dataclass
class FileAttachment(MediaAttachment):
    """
    Вложение с файлом
    """
    filename: str
    size: int
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(
            type='file',
            id=data.get('id', ''),
            url=data.get('url', '')
        )
        self.filename = data.get('filename', '')
        self.size = data.get('size', 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует файл в словарь
        """
        return {
            **super().to_dict(),
            'filename': self.filename,
            'size': self.size
        }

@dataclass
class StickerAttachment(BaseAttachment):
    """
    Вложение со стикером
    """
    sticker_id: str
    emoji: Optional[str] = None
    
    def __init__(self, sticker_id: str, emoji: Optional[str] = None):
        super().__init__(type='sticker')
        self.sticker_id = sticker_id
        self.emoji = emoji
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует стикер в словарь
        """
        result = {
            **super().to_dict(),
            'sticker_id': self.sticker_id
        }
        
        if self.emoji:
            result['emoji'] = self.emoji
            
        return result

@dataclass
class LocationAttachment(BaseAttachment):
    """
    Вложение с геолокацией
    """
    latitude: float
    longitude: float
    
    def __init__(self, latitude: float, longitude: float):
        super().__init__(type='location')
        self.latitude = latitude
        self.longitude = longitude
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует геолокацию в словарь
        """
        return {
            **super().to_dict(),
            'latitude': self.latitude,
            'longitude': self.longitude
        }

@dataclass
class ShareAttachment(BaseAttachment):
    """
    Вложение с данными
    """
    data: Dict[str, Any]
    
    def __init__(self, share_type: str, data: Dict[str, Any]):
        super().__init__(type=share_type)
        self.data = data
    
    @property
    def contact(self) -> Optional[Dict[str, Any]]:
        """
        Извлекает контактную информацию
        """
        if self.type == 'contact':
            return self.data
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует данные в словарь
        """
        return {
            **super().to_dict(),
            **self.data
        } 