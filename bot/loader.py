import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from config import TOKEN
from init_db import create_pool


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# Set up storage
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage, loop=asyncio.get_event_loop())
db = dp.loop.run_until_complete(create_pool())
