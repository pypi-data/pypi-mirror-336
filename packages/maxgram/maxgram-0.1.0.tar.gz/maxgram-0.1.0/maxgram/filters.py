from typing import Any, Callable, TypeVar

T = TypeVar('T')

def created_message_body_has(property_name: str) -> Callable[[Any], bool]:
    """
    Создает фильтр, который проверяет наличие свойства в теле сообщения
    """
    def filter_fn(update: Any) -> bool:
        if update.update_type != 'message_created':
            return False
            
        if not hasattr(update, 'message') or not update.message:
            return False
            
        if not hasattr(update.message, 'body') or not update.message.body:
            return False
            
        return hasattr(update.message.body, property_name)
        
    return filter_fn 