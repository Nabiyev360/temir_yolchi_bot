from aiogram import types

from loader import dp
from data.config import ADMINS


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    # await message.answer(message.text)
    try:
        await message.forward(ADMINS[0])
    except:
        pass