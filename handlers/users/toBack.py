from aiogram.types import CallbackQuery

from loader import dp, db
from keyboards.default.mainKeyboard import main_keyboard
from keyboards.inline.categories import category_keyboard



@dp.callback_query_handler(text= 'to main')
async def toMain(call: CallbackQuery):
	await call.message.delete()
	await call.message.answer(text= "Asosiy menu", reply_markup=main_keyboard)


@dp.callback_query_handler(text= 'to categories')
async def toCategories(call: CallbackQuery):
	await call.message.edit_text('Savollar kategoriyasini tanlang:', reply_markup= category_keyboard)