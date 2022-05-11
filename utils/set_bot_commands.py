from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        #types.BotCommand("help", "Помощь"),
        types.BotCommand("info", "Инфо"),
        types.BotCommand("new", "Новая заявка"),
        types.BotCommand("requests", "Последние 5 заявок"),
        types.BotCommand("req", "Узнасть статус заявки"),
    ])
