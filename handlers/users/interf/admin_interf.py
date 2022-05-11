from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import message
from loader import dp 
from utils.db_api.db_commands import select_all_users

async def info(message: types.Message):
    await message.answer("Бот для отпраки моделей на печать, Вы Админ")
    res = await select_all_users()
    await message.answer(f"Всего ползователей : {len(res)} ")