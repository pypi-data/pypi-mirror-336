import re
from typing import Any, Callable, List, Optional, Pattern, TypeVar, Union, overload

from .core.helpers.types import Guard, MaybeArray
from .core.network.api import Message, UpdateType

from .middleware import Middleware, MiddlewareFn, MiddlewareObj, NextFn
from .context import Context, FilteredContext
from .filters import created_message_body_has

Triggers = Union[str, Pattern, List[Union[str, Pattern]]]
UpdateFilter = Union[UpdateType, Guard]

C = TypeVar('C', bound=Context)

class Composer(MiddlewareObj[C]):
    """
    Класс для компоновки обработчиков событий
    """
    
    def __init__(self, *middlewares: Middleware[C]):
        self.handler = Composer.compose(middlewares)
    
    def middleware(self) -> MiddlewareFn[C]:
        """
        Возвращает обработчик middleware
        """
        return self.handler
    
    def use(self, *middlewares: Middleware[C]):
        """
        Добавляет middleware для обработки событий
        """
        self.handler = Composer.compose([self.handler, *middlewares])
        return self
    
    @overload
    def on(self, filter_type: UpdateType, *middlewares: Middleware[Any]) -> 'Composer[C]':
        ...
        
    @overload
    def on(self, filters: MaybeArray[Guard[Any]], *middlewares: Middleware[Any]) -> 'Composer[C]':
        ...
    
    def on(self, filters, *middlewares):
        """
        Добавляет обработчики для определенного типа событий
        """
        return self.use(self.filter(filters, *middlewares))
    
    def command(self, command: Triggers, *middlewares):
        """
        Добавляет обработчики для команд (начинающихся с /)
        """
        normalized_triggers = self._normalize_triggers(command)
        message_filter = created_message_body_has('text')
        
        handler = Composer.compose(middlewares)
        
        return self.use(self.filter(message_filter, lambda ctx, next_fn: (
            self._process_command(ctx, next_fn, normalized_triggers, handler)
        )))
    
    async def _process_command(self, ctx, next_fn, triggers, handler):
        text = self._extract_text_from_message(ctx.message, ctx.my_id)
        if not text or not text.startswith('/'):
            return await next_fn()
            
        cmd = text[1:]  # Удаляем слеш в начале
        
        for trigger in triggers:
            match = trigger(cmd)
            if match:
                ctx.match = match
                return await handler(ctx, next_fn)
                
        return await next_fn()
    
    def hears(self, triggers: Triggers, *middlewares):
        """
        Добавляет обработчики для текстовых сообщений
        """
        normalized_triggers = self._normalize_triggers(triggers)
        message_filter = created_message_body_has('text')
        
        handler = Composer.compose(middlewares)
        
        return self.use(self.filter(message_filter, lambda ctx, next_fn: (
            self._process_text(ctx, next_fn, normalized_triggers, handler)
        )))
    
    async def _process_text(self, ctx, next_fn, triggers, handler):
        text = self._extract_text_from_message(ctx.message, ctx.my_id)
        if not text:
            return await next_fn()
            
        for trigger in triggers:
            match = trigger(text)
            if match:
                ctx.match = match
                return await handler(ctx, next_fn)
                
        return await next_fn()
    
    def action(self, triggers: Triggers, *middlewares):
        """
        Добавляет обработчики для callback действий
        """
        normalized_triggers = self._normalize_triggers(triggers)
        handler = Composer.compose(middlewares)
        
        return self.use(self.filter('message_callback', lambda ctx, next_fn: (
            self._process_action(ctx, next_fn, normalized_triggers, handler)
        )))
    
    async def _process_action(self, ctx, next_fn, triggers, handler):
        payload = ctx.update.callback.payload
        
        if not payload:
            return await next_fn()
            
        for trigger in triggers:
            match = trigger(payload)
            if match:
                ctx.match = match
                return await handler(ctx, next_fn)
                
        return await next_fn()
    
    def filter(self, filters, *middlewares):
        """
        Создает middleware, который фильтрует события
        """
        handler = Composer.compose(middlewares)
        
        async def middleware(ctx: C, next_fn: NextFn):
            return await handler(ctx, next_fn) if ctx.has(filters) else await next_fn()
            
        return middleware
    
    @staticmethod
    def flatten(mw: Middleware[C]) -> MiddlewareFn[C]:
        """
        Преобразует middleware в функцию
        """
        if callable(mw) and not hasattr(mw, 'middleware'):
            return mw
        return mw.middleware()
    
    @staticmethod
    async def concat(first: MiddlewareFn[C], second: MiddlewareFn[C], ctx: C, next_fn: NextFn):
        """
        Объединяет два middleware в один
        """
        next_called = False
        
        async def next_wrapper():
            nonlocal next_called
            if next_called:
                raise RuntimeError('`next` уже был вызван ранее!')
            next_called = True
            await second(ctx, next_fn)
            
        await first(ctx, next_wrapper)
    
    @staticmethod
    async def pass_through(ctx: C, next_fn: NextFn):
        """
        Пропускает вызов к следующему middleware
        """
        await next_fn()
    
    @staticmethod
    def compose(middlewares: List[Middleware[C]]) -> MiddlewareFn[C]:
        """
        Объединяет список middleware в одну функцию
        """
        if not isinstance(middlewares, list):
            raise TypeError('middlewares должен быть списком')
            
        if len(middlewares) == 0:
            return Composer.pass_through
            
        flattened = [Composer.flatten(mw) for mw in middlewares]
        
        async def composed_middleware(ctx: C, next_fn: NextFn):
            async def execute_middleware(index: int):
                if index >= len(flattened):
                    await next_fn()
                    return
                
                await flattened[index](ctx, lambda: execute_middleware(index + 1))
                
            await execute_middleware(0)
            
        return composed_middleware
    
    def _normalize_triggers(self, triggers: Triggers) -> List[Callable[[str], Optional[re.Match]]]:
        """
        Нормализует триггеры в список функций для проверки совпадений
        """
        if not isinstance(triggers, list):
            triggers = [triggers]
            
        result = []
        for trigger in triggers:
            if isinstance(trigger, re.Pattern):
                result.append(lambda value, pattern=trigger: pattern.search(value or ''))
            else:
                pattern = re.compile(f'^{re.escape(trigger)}$')
                result.append(lambda value, pattern=pattern: pattern.search(value or ''))
                
        return result
    
    def _extract_text_from_message(self, message: Message, my_id: Optional[int] = None) -> Optional[str]:
        """
        Извлекает текст из сообщения, обрабатывая упоминания
        """
        text = message.body.text
        
        if not text:
            return None
            
        if hasattr(message.body, 'markup'):
            mention = next((
                m for m in message.body.markup 
                if m.type == 'user_mention' and m.from_ == 0 and m.user_id == my_id
            ), None)
            
            if mention:
                return text[mention.length:].strip()
                
        return text 