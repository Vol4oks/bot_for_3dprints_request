from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import message
from loader import dp

async def info(message: types.Message):
    await message.answer("Бот для отпраки моделей на печать")




