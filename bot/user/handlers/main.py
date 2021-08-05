from aiogram import types
from aiogram.dispatcher import FSMContext
from ..keyboards import kb_main
import logging
from loader import dp, bot
from parser import CryptoPanic, CoinMarketCap
from config import CHANNEL_ID, ADMINS


@dp.message_handler(lambda msg: msg.from_user.id in ADMINS, commands=['start'], state='*')
async def starting(message: types.Message, state: FSMContext):
    """Answer "/start"."""
    text = 'What can I help you with?\n'
    await bot.send_message(message.from_user.id, text, reply_markup=kb_main)


@dp.callback_query_handler(lambda c: c.data in ['hot', 'bullish', 'bearish', 'important'])
async def send_news_cp(call: types.CallbackQuery, state: FSMContext):
    """send news."""
    logging.info('Process news request')
    text = CryptoPanic().format_data(call.data)
    try:
        logging.info('Sent')
        # await call.message.answer(text=text, disable_web_page_preview=True)
        await bot.send_message(chat_id=CHANNEL_ID, text=text, disable_web_page_preview=True)
    except Exception as er:
        logging.info(er)
    return


@dp.callback_query_handler(lambda c: c.data in ['losers', 'gainers', 'trending', 'stats'])
async def send_news_cmc(call: types.CallbackQuery, state: FSMContext):
    """send news."""
    logging.info('Process news request')
    text = CoinMarketCap().format_data(call.data)
    try:
        logging.info('Sent')
        # await call.message.answer(text=text, disable_web_page_preview=True)
        await bot.send_message(chat_id=CHANNEL_ID, text=text, disable_web_page_preview=True)
    except Exception as er:
        logging.info(er)
    return


@dp.callback_query_handler(lambda c: c.data == 'about')
async def send_news_cmc(call: types.CallbackQuery, state: FSMContext):
    """tell about the bot."""
    logging.info('Process about request')
    text = 'Hi! I will help you to track crypto news, etc.\nFor trading ideas join @Pro_Crypto_Signals'
    try:
        logging.info('Sent')
        await call.message.answer(text=text, disable_web_page_preview=True)
        # await bot.send_message(chat_id=CHANNEL_ID, text=text, disable_notification=True)

    except Exception as er:
        logging.info(er)
    return
