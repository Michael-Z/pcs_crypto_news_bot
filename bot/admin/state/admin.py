from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    SetCode = State()
    ManageTexts = State()
    UpdateButton = State()
