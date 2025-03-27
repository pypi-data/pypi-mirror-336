import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from .api import Api, Update, UpdateType

logger = logging.getLogger('maxbot-api')

class Polling:
    """
    Класс для работы с long polling
    """
    
    def __init__(
        self, 
        api: Api, 
        allowed_updates: Optional[List[UpdateType]] = None,
        limit: int = 100,
        timeout: int = 30
    ):
        self.api = api
        self.allowed_updates = allowed_updates
        self.limit = limit
        self.timeout = timeout
        
        self._is_running = False
        self._offset: Optional[str] = None
    
    async def loop(self, handler: Callable[[Update], Any]) -> None:
        """
        Запускает цикл получения обновлений
        """
        if self._is_running:
            logger.warning("Polling loop already running")
            return
            
        self._is_running = True
        self._offset = None
        
        logger.debug("Starting polling loop")
        
        while self._is_running:
            try:
                updates = await self._get_updates()
                
                for update in updates:
                    asyncio.create_task(self._process_update(update, handler))
                    
                if updates and len(updates) > 0:
                    self._offset = updates[-1].get('offset')
                    
            except Exception as e:
                logger.error(f"Error in polling: {e}")
                # Небольшая задержка перед следующей попыткой
                await asyncio.sleep(3)
    
    def stop(self) -> None:
        """
        Останавливает цикл получения обновлений
        """
        logger.debug("Stopping polling loop")
        self._is_running = False
    
    async def _get_updates(self) -> List[Dict[str, Any]]:
        """
        Получает обновления с сервера
        """
        data = {
            'limit': self.limit,
            'timeout': self.timeout
        }
        
        if self._offset:
            data['offset'] = self._offset
            
        result = await self.api.get_updates(self.allowed_updates, data)
        return result.get('updates', [])
    
    async def _process_update(self, update: Dict[str, Any], handler: Callable[[Update], Any]) -> None:
        """
        Обрабатывает полученное обновление
        """
        try:
            await handler(update)
        except Exception as e:
            logger.error(f"Error processing update: {e}") 