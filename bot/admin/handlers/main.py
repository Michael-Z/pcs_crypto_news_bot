from aiogram import types
from aiogram.dispatcher import FSMContext

from config import IP_WHITELIST
from loader import dp, bot


@dp.message_handler(lambda message: message.from_user.id in IP_WHITELIST,
                    commands=['admin'], state='*')
async def admin_panel(message: types.Message, state: FSMContext):
    """Process /admin, send admin-panel."""
    await bot.send_message(chat_id=message.from_user.id, text='Admin panel!')
