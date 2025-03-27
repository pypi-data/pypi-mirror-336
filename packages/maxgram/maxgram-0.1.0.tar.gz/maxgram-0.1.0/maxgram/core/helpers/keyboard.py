from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

@dataclass
class InlineKeyboard:
    """
    Клавиатура с интерактивными кнопками
    """
    rows: List[List[Dict[str, Any]]]
    
    def __init__(self, rows: List[List[Dict[str, Any]]]):
        self.rows = rows
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует клавиатуру в словарь
        """
        return {
            'type': 'inline_keyboard',
            'rows': self.rows
        }

class button:
    """
    Класс для создания кнопок
    """
    
    @staticmethod
    def link(text: str, url: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создает кнопку-ссылку
        """
        extra = extra or {}
        return {
            'type': 'link',
            'text': text,
            'url': url,
            **extra
        }
    
    @staticmethod
    def callback(text: str, payload: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создает кнопку с callback-запросом
        """
        extra = extra or {}
        return {
            'type': 'callback',
            'text': text,
            'payload': payload,
            **extra
        }
    
    @staticmethod
    def request_geo_location(text: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создает кнопку для запроса геолокации
        """
        extra = extra or {}
        return {
            'type': 'request_geo_location',
            'text': text,
            **extra
        }
    
    @staticmethod
    def request_contact(text: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создает кнопку для запроса контактных данных
        """
        extra = extra or {}
        return {
            'type': 'request_contact',
            'text': text,
            **extra
        }
    
    @staticmethod
    def chat(text: str, title: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создает кнопку для создания чата
        """
        extra = extra or {}
        return {
            'type': 'chat',
            'text': text,
            'chat': {
                'title': title
            },
            **extra
        }

def inline_keyboard(rows: List[List[Dict[str, Any]]]) -> InlineKeyboard:
    """
    Создает inline-клавиатуру
    """
    return InlineKeyboard(rows)
 