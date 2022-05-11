from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import GetStatus
from utils.db_api.db_commands import get_requests, get_status, select_user


@dp.message_handler(text="/requests")
async def return_request(message: types.Message):
    usr = await select_user(message.from_user.id)
    ans = await get_requests(usr.id)
    await message.answer(f"Ваши запросы:")
    for i in ans:
        await message.answer(f"{i}")

@dp.message_handler(text="/req", state=None)
async def start_return_request(message: types.Message):
    await message.answer("Введите номер заявки")
    await GetStatus.q1.set()

@dp.message_handler(state=GetStatus.q1)
async def return_request(message: types.Message, state: FSMContext):
    mes = message.text
    if mes.isdigit():
        ans = await get_status(mes)
        await message.answer(f"Статус заказа {mes}: \n {ans}")
        await state.reset_state()
    else:
        await message.answer("Не понял вас")

        