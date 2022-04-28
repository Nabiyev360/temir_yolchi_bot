from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_battle_keyboard(battle_id):
    keyboard= InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text= 'Bellashuvni boshlash', 
        callback_data=f"start-{battle_id}"
        )
    )
    return keyboard