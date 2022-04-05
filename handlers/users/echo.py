from aiogram import types
from loader import dp
from data.config import admins
from aiogram.types import message
from .interf import admin_interf, users_inerf

@dp.message_handler(text='/info')
async def show_info(message: types.Message):
    if message.from_user.id in admins:
        await admin_interf.info(message)
    else:
        await users_inerf.info(message)

@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
