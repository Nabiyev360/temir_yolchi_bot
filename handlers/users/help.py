from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from keyboards.inline.handbook import handbook_button



@dp.message_handler(CommandHelp())
@dp.message_handler(text="📜 Qo'llanma")
async def bot_help(message: types.Message):
    text = ("👳🏻‍♂️ Siz <a href='https://telegra.ph/islomiy-bellashuv-bot--Qanday-foydalanamiz-04-06'>ushbu sahifa</a>da botdan foydalanish bo'yicha to'liq ma'lumotga ega bo'lasiz.",
            "Qo'shimcha ma'lumotlar uchun @nabiyevdev")
    
    await message.reply("\n\n".join(text),
        disable_web_page_preview=True,
        reply_markup=handbook_button)