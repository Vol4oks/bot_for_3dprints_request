from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.db_commands import select_user, add_user
from states.step_request_for import NewUser

@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    user = await select_user(message.from_user.id)
    if not user:
        await message.answer(f"Привет! Тебя зовут {message.from_user.full_name}?")
        await message.answer("Если да - ответь да.\n Если нет - напиши как тебя зовут.")
        await NewUser.start.set()
    else:
        await message.answer(f"Привет: {user.name}")

@dp.message_handler(state=NewUser.start)
async def change_name(message: types.Message, state: FSMContext):
    anser = message.text
    if message.text.lower() == "да":
        anser = message.from_user.full_name

    await add_user(user_id=message.from_user.id, 
                        full_name=anser, 
                        username=message.from_user.username)
    await message.answer(f"Привет {anser}")
    await state.reset_state()