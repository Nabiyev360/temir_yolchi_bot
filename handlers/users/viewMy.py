from aiogram.types import CallbackQuery
from loader import dp, db

from data.config import ADMINS
from keyboards.default.mainKeyboard import main_keyboard
from extra import short_category


@dp.callback_query_handler(text_contains = 'view-')
async def view_my_result(call: CallbackQuery):
	user_id= call.from_user.id
	name = call.from_user.full_name
	battle_id = call.data[5:]
	
	try:
		result_one = db.get_my_result(battle_id, user_id)
		category = short_category[result_one[3]]

		if user_id == result_one[1]:
			check = result_one[5][:10]
			corrects_count = result_one[5][:10].count('✅')
			wrongs_count = result_one[5][:10].count('❌')
		
		elif user_id == result_one[2]:
			check = result_one[6][:10]
			corrects_count = result_one[6][:10].count('✅')
			wrongs_count = result_one[6][:10].count('❌')

		msg = f"<b>{category}</b> bo'yicha" + '\n🧾#natija ' + name + f"\n\n✅To'g'ri javoblar - {corrects_count} ta" + f"\n❌Notog'ri javoblar - {wrongs_count} ta" + '\n\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟\n' + check

		await call.message.answer(msg, reply_markup=main_keyboard)
	
	except Exception as ex:
		await call.answer("Texnik xatolik yuz berdi", show_alert=True)
		await dp.bot.send_message(ADMINS[0], ex)

	await call.message.delete()