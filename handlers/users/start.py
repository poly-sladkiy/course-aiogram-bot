import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

    not_existing_user_id = 666666

    # Не будет отправлен в error handler, а обработаетсся здесь
    try:
        await message.answer('Неверно закрытый <b>тег<b>')
    except Exception as err:
        await message.answer(f"Не попало в error handler.\n"
                             f"Ошибка: <code>{err}</code>")

    # Не попадет в error handler
    try:
        await bot.send_message(chat_id=not_existing_user_id, text='Не существующий акк')
    except Exception as err:
        await message.answer(f'Сообщение не попало в error handler.\n'
                             f'Ошибка: <code>{err}</code>')

    # Попадет в error handler
    await message.answer('Не существующий <kek>тег</kek>')

    # Не выполнится всё что ниже
    logging.info('Это не выполнится, бот не упадёт, ошибка ушла в error handler')

    await message.answer('...')
