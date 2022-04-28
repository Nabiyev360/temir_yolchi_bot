from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.mainKeyboard import main_keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Assalomu alaykum {message.from_user.first_name}!",
        reply_markup=main_keyboard)

    db.add_user(
        message.from_user.id, 
        message.from_user.first_name, 
        message.from_user.last_name, 
        message.from_user.username)