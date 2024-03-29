from utils.set_bot_commands import set_default_commands

import os
import django
from admin_django.admin_django import settings

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

def setup_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "admin_django.admin_django.settings"

    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()



if __name__ == '__main__':
    setup_django()

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
