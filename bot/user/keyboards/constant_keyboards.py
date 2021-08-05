from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='About', callback_data='about'),
        InlineKeyboardButton(text='Hot news', callback_data='hot')
    ],
    [
        InlineKeyboardButton(text='Bullish news', callback_data='bullish'),
        InlineKeyboardButton(text='Bearish news', callback_data='bearish')
    ],
    [
        InlineKeyboardButton(text='Biggest Losers', callback_data='losers'),
        InlineKeyboardButton(text='Biggest Gainers', callback_data='gainers')
    ],
    [
        InlineKeyboardButton(text='Important', callback_data='important'),
        InlineKeyboardButton(text='Trending', callback_data='trending')
    ],
    [
        InlineKeyboardButton(text='Market Stats', callback_data='stats'),
    ],
])
