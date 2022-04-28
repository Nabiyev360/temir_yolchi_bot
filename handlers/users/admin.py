import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db
from states.adminStates import AdminState
from keyboards.inline.adminCancel import admin_cancel

@dp.message_handler(user_id = ADMINS, text = ['/help_admin'])
async def send_message_users(message: types.Message):
    await message.answer(f"/count - Foydalanuvchilar soni\n\
/count_group - Bot qo'shilgan guruhlar soni\n\
/message - Foydalanuvchilarga xabar yuborish\n\
/get_words - Bazadagi so'zlar excel formatda\n\
/add_channel - Majburiy a'zolik kanal qo'shish\n\
/example - So'z qo'shish uchun misol")

# Reklama yuborish
@dp.message_handler(user_id = ADMINS, text = "/message")
async def send_message_users(message: types.Message):
    await message.answer(text = "Foydalanuvchilarga yuborish kerak bo'lgan xabarni yuboring🔼\n\nBekor qilish uchun \"Cancel\"ni bosing",
        reply_markup = admin_cancel)
    await AdminState.waiting_admin_message.set()

@dp.message_handler(user_id = ADMINS, state = AdminState.waiting_admin_message, content_types= types.ContentType.ANY)
async def send_message_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Xabar foydalanuvchilarga yuborilmoqda...')
    n = 0
    for i in db.get_users_id():
        user_id = i[0]
        try:
            await message.send_copy(chat_id = user_id)
            n+=1
        except:
            pass
        await asyncio.sleep(0.5)
    await message.answer(f'Xabar {n} ta foydalanuvchiga muvaffaqqiyatli yuborildi!')



@dp.message_handler(user_id = ADMINS, text = "/count")
async def send_count_users(message: types.Message):
    await message.answer(db.count_users())


# send database file to admin
@dp.message_handler(user_id = ADMINS, text = ["/getdb", 'getdb'])
async def send_datafile(message: types.Message):
    file = open('data/quiz.db', 'rb')
    await message.answer_document(file)
    file.close()

@dp.message_handler(user_id = ADMINS, text = ["/getusers", 'getusers'])
async def send_datafile(message: types.Message):
    file = open('data/users.db', 'rb')
    await message.answer_document(file)
    file.close()

@dp.message_handler(user_id = ADMINS, text = ["/getbattles", 'getbattles'])
async def send_datafile(message: types.Message):
    file = open('data/battles.db', 'rb')
    await message.answer_document(file)
    file.close()


@dp.callback_query_handler(user_id = ADMINS, state = '*', text = 'cancel_admin')
async def cancel_send_msg(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Bekor qilindi!")


@dp.message_handler(user_id = ADMINS, content_types=['document'])
async def admin_file(message: types.Message):
    file_name = message.document.file_name
    if file_name == 'quiz.db':
        file_id = message.document.file_id
        file = await dp.bot.get_file(file_id)   
        file_path = 'quiz.db'
        await dp.bot.download_file(file_path, file_name)
        await message.answer("Savollar ombori yangilandi!")