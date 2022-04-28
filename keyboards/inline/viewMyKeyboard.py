from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def view_my_keyboard(battle_id):
	keyboard= InlineKeyboardMarkup()
	keyboard.add(
		InlineKeyboardButton(
			text="Natijamni ko'rish 👀", 
			callback_data=f'view-{battle_id}'
			)
		)
	keyboard.add(
		InlineKeyboardButton(
			text="Asosiy menyu",
			callback_data= 'to main'))
	return keyboard