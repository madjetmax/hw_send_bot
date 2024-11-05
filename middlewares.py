from aiogram import BaseMiddleware, Dispatcher, Router
from aiogram.types import Message, TelegramObject, ChatMemberUpdated
from sqlalchemy.ext.asyncio import async_sessionmaker
from database import DataBase
from bot_data import bot_data


from typing import Any, Coroutine, Dict, Callable, Awaitable
import logging, config, json
from cachetools import TTLCache

db = DataBase()

class MaiMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=4)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        
        if event.text == "/admin":
            admins = bot_data.admins
            if event.from_user.id in admins:
                return await handler(event, data)
            
        banned_users = bot_data.banned_users
        if event.from_user.id not in banned_users:
            return await handler(event, data)
        return 


