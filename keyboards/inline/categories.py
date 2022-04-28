from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from extra import categories

category_keyboard = InlineKeyboardMarkup()

for i in categories:
    category_keyboard.add(InlineKeyboardButton(i, callback_data= categories[i]))

category_keyboard.add(InlineKeyboardButton('🔙 Orqaga', callback_data= 'to main'))