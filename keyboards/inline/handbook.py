from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

handbook_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text= "👉Sahifaga o'tish", url= "https://telegra.ph/islomiy-bellashuv-bot--Qanday-foydalanamiz-04-06"))

handbook_button.add(InlineKeyboardButton('🔙 Orqaga', callback_data= 'to main'))