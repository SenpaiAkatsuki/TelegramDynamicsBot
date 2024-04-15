from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class DialogMiddleware(BaseMiddleware):
    def __init__(self, registry) -> None:
        self.registry = registry

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['registry'] = self.registry
        return await handler(event, data)
