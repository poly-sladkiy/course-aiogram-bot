from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from aiogram import types

from states import Test


@dp.message_handler(Command("test"), state=None)
async def enter_test(message: types.Message):
    """
         Можно прописать:
        1.  text='/test'
        2.  Command('test')

    """

    await message.answer('Это вопрос 1')

    # await Test.Q1.set()
    await Test.first()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(answer1=answer)

    # await state.update_data({
    #     'answer1': answer
    # })

    async with state.proxy() as data:
        data['answer1'] = answer

    await message.answer('Это вопрос 2')
    await Test.next()

    # await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()

    answer1 = data.get('answer1')
    answer2 = message.text

    await message.answer('Тест закончился.')
    await message.answer(f'1 ответ: {answer1}')
    await message.answer(f'2 ответ: {answer2}')

    await state.finish()
    # await state.reset_state()

    # чтобы сбросить состояние, но оставить ответы на вопросы:
    # await state.reset_state(with_data=False)
