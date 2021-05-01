from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api.user import User


# Не достаточно просто создать этот класс
# его не обходимо установить в __init__.py
class GetDBUser(BaseMiddleware):

    async def on_process_message(self, message: types.Message,
                                 data=dict):
        """
        :data: то что потом летит в handler
            это словарь, в котором мы можем
            создать новое поле, а в handler
            использовать его
        """

        data['user'] = User(_id=message.from_user.id,
                            _name=message.from_user.full_name)

    async def on_process_callback_query(self, cq: types.CallbackQuery,
                                        data: dict):

        data['user'] = User(_id=cq.from_user.id,
                            _name=cq.from_user.full_name)
