from aiogram.types import Message, CallbackQuery
import ast

from loader import dp, db
from extra import categories, short_category, make_variant
from keyboards.inline.revanshButton import revansh_req
from keyboards.inline.startBattleKeyboard import start_battle_keyboard

from data.config import ADMINS


@dp.callback_query_handler(text_contains= ", '")    # revanshButton > revansher
async def revansher(call: CallbackQuery):    
    # print(call)
    name= call.from_user.first_name
    username= call.from_user.username
    user_id= call.from_user.id
    data= call.data
    enemy_id= ast.literal_eval(data)[0]
    category= ast.literal_eval(data)[1]

    for i in categories:
        if categories[i] == category:
            category_full= i

    msg= f"Salom, sizni foydalanuvchi <b><a href='https://t.me/{username}'>{name}</a></b> <b>{category_full}</b> to'plami bo'yicha o'tkazilgan bellashuvga ko'ra Revansh bellashuvga chaqiryapti, qabul qilasizmi?"

    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer("Revansh taklifi raqibga yuborildi!", show_alert=True)
    await dp.bot.send_message(
        chat_id=enemy_id,
        text= msg, 
        reply_markup=revansh_req(user_id),
        disable_web_page_preview=True
    )


@dp.callback_query_handler(text_contains= "re-agree-")
async def agree(call: CallbackQuery):
    # print(call)
    requirer_id= int(call.data[9:])
    agreer_id= call.from_user.id
    agreer_name= call.from_user.first_name
    username= call.from_user.username
    
    offset= call.message.entities[2].offset
    length= call.message.entities[2].length

    # category_full va category'ni aniqlash
    message= call.message.text
    for longctg in categories:
        if longctg in message:
            category_full= longctg
            category= categories[category_full]

    # category_full= call.message.text[offset : offset+length]
    # category= categories[category_full[:-1]]
    msg= f"✅ <a href='https://t.me/{username}'>{agreer_name}</a> taklifni qabul qildi"

    try:
        await dp.bot.send_message(
            chat_id= requirer_id, 
            text= msg,
            disable_web_page_preview=True)
        
        await call.message.edit_text(
            text= msg,
            disable_web_page_preview=True)

        variant= make_variant(category)
        new_battle_id= db.new_revansh_battle(
            user1_id= agreer_id,
            user2_id= requirer_id, 
            category= category, 
            tests= variant)
        
        msg= f"<b>{category_full}</b><a href='https://{category}.uz'> </a>bo'yicha bellashuvni boshlash uchun quyidagi tugmani bosing.\n\nTestlar soni 10 ta, bellashuvda kim g'alaba qilsa unga 10 💎 taqdim etiladi."
            
        await dp.bot.send_message(
            chat_id= requirer_id,
            text= msg,
            reply_markup=start_battle_keyboard(new_battle_id))
        
        await call.message.answer(
            text= msg,
            reply_markup=start_battle_keyboard(new_battle_id))
    
    except Exception as ex:
        await call.answer("Foydalanuvchi topilmadi!", show_alert=True)
        # print(ex)
        await dp.bot.send_message(chat_id=ADMINS[0], text= ex)



@dp.callback_query_handler(text_contains= "disagree-")
async def revansher2(call: CallbackQuery):
    requirer_id= int(call.data[9:])
    agreer_name= call.from_user.first_name
    username= call.from_user.username

    msg= f"❌ <a href='https://t.me/{username}'>{agreer_name}</a> taklifni rad qildi"

    try:
        await dp.bot.send_message(
            chat_id= requirer_id, 
            text= msg,
            disable_web_page_preview=True)
    except:
        pass
    
    await call.message.edit_text(
        text= msg,
        disable_web_page_preview=True)
    
    # await call.message.delete()