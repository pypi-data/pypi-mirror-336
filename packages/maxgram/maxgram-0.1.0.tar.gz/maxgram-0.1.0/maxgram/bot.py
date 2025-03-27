import logging
import asyncio
from typing import Awaitable, Callable, Optional, Type, TypeVar

from .composer import Composer
from .context import Context
from .api import MaxAPI

from .core.network.api import (
    BotInfo, ClientOptions, create_client, Update, UpdateType
)
from .core.network.polling import Polling

logger = logging.getLogger('maxbot-api')

MaybePromise = Awaitable[None] | None

class BotConfig:
    def __init__(
        self, 
        client_options: Optional[ClientOptions] = None,
        context_type: Type[Context] = Context
    ):
        self.client_options = client_options
        self.context_type = context_type

C = TypeVar('C', bound=Context)

class Bot(Composer[C]):
    """
    Основной класс бота для обработки событий и взаимодействия с API
    """
    
    def __init__(self, token: str, config: Optional[BotConfig] = None):
        super().__init__()
        
        self.config = config or BotConfig()
        self.api = MaxAPI(create_client(token, self.config.client_options))
        self.bot_info = None
        self.polling = None
        self.polling_is_started = False
        
        logger.debug('Created Bot instance')
    
    async def _handle_error(self, err: Exception, ctx: C) -> MaybePromise:
        """
        Обработчик ошибок по умолчанию
        """
        import sys
        sys.exit(1)
        logger.error('Unhandled error while processing %s', ctx.update)
        raise err

    def catch(self, handler: Callable[[Exception, C], MaybePromise]):
        """
        Устанавливает пользовательский обработчик ошибок
        """
        self._handle_error = handler
        return self
    
    async def start(self, allowed_updates: Optional[list[UpdateType]] = None):
        """
        Запускает бота в режиме long polling
        """
        if self.polling_is_started:
            logger.debug('Long polling already running')
            return
        
        self.polling_is_started = True
        
        if self.bot_info is None:
            self.bot_info = await self.api.get_my_info()
        
        self.polling = Polling(self.api, allowed_updates)
        
        logger.debug(f'Starting @{self.bot_info.username}')
        await self.polling.loop(self._handle_update)
    
    def stop(self):
        """
        Останавливает бота
        """
        if not self.polling_is_started:
            logger.debug('Long polling is not running')
            return
        
        if self.polling:
            self.polling.stop()
        
        self.polling_is_started = False
    
    async def _handle_update(self, update: Update):
        """
        Обрабатывает входящие обновления
        """
        update_id = f"{update.update_type}:{update.timestamp}"
        logger.debug(f'Processing update {update_id}')
        
        UpdateContext = self.config.context_type
        ctx = UpdateContext(update, self.api, self.bot_info)
        
        try:
            await self.middleware()(ctx, lambda: asyncio.create_task(asyncio.sleep(0)))
        except Exception as err:
            await self._handle_error(err, ctx)
        finally:
            logger.debug(f'Finished processing update {update_id}') 