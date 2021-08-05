import asyncio
import logging

import asyncpg
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import host, PG_PASS, PG_USER, TOKEN

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# Set up storage
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage, loop=asyncio.get_event_loop())


async def create_pool():
    return await asyncpg.create_pool(user=PG_USER,
                                     password=PG_PASS,
                                     host=host)


db = dp.loop.run_until_complete(create_pool())
