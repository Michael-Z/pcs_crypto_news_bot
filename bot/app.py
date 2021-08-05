from aiogram import executor
import asyncio
from config import admin_id
from loader import bot
import os
from aiogram.utils.exceptions import ChatNotFound
import logging


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await asyncio.sleep(2)
    try:
        await bot.send_message(admin_id, "I have started up!")
    except ChatNotFound:
        logging.info('Admin chat not found')


if __name__ == '__main__':
    from user import dp
    from admin import dp

    os.system('chmod +x init_db.py')
    os.system('python3.8 init_db.py')
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
