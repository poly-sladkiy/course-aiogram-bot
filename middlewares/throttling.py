import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        # Чтобы мы не отвечали человеку throttled.rate секунд между двумя последними командами
        # delta = throttled.rate - throttled.delta

        # Если сообщени прислали 2 раза
        if throttled.exceeded_count <= 2:
            await message.reply("Too many requests!")

        # Если сообщени прислали 3 раза
        # throttled.rate - количество секунд для определенной функции
        # Если вызвать self.rate_limit, оно всегда .1 сек
        if throttled.exceeded_count == 3:
            await message.reply(f'You have a ban for <code>{throttled.rate}</code> seconds!\n'
                                f'key: <code>{throttled.key}</code>')
        # await asyncio.sleep(delta)
        # await message.answer("Ban is end!")
