from aiogram import types

from loader import dp, db
from extra import short_category
from keyboards.inline.typeKeyboard import friend_req
from keyboards.inline.startBattleKeyboard import start_battle_keyboard
from extra import make_variant


def msger(name, username, category):
    return f"<b>Salom</b>, foydalanuvchi <b><a href='https://t.me/{username}'>{name}</a></b> sizni <i><b>{category}</b></i> bo'yicha bellashuvga taklif etdi. Munosabat bildirish uchun quyidagi tugmalardan foydalaning.\n\nBellashuvni qabul qilganingizda taklif etuvchi va sizga bellashuvni boshlash imkonini beruvchi yangi xabar @temir_yolchi_bot tomonidan yuboriladi va siz ushbu xabarga biriktirilgan tugma yordamida bellashuvni boshlashingiz mumkin bo'ladi."

@dp.inline_handler(text=short_category)
async def with_friend(query: types.InlineQuery):
    name= query.from_user.first_name
    username= query.from_user.username
    user_id= query.from_user.id
    query_category= query.query
    
    inline_results= []
    inline_results.append(types.InlineQueryResultArticle(
            id=query_category,
            title= query_category.upper(),
            input_message_content = types.InputTextMessageContent(
                message_text=msger(name, username, category=short_category[query_category]),
                disable_web_page_preview=True
            ),
            description=short_category[query_category],
            reply_markup=friend_req(user_id, query_category)
        )
    )
    await query.answer(inline_results)

@dp.inline_handler()
async def with_friend(query: types.InlineQuery):
    name= query.from_user.first_name
    username= query.from_user.username
    user_id= query.from_user.id
    
    inline_results= []
    for i in short_category:
        inline_results.append(
            types.InlineQueryResultArticle(
                id= i,
                title= i.upper(),
                input_message_content = types.InputTextMessageContent(
                    message_text=msger(name, username, category=short_category[i]),
                    disable_web_page_preview=True
                ),
                description=short_category[i],
                reply_markup=friend_req(user_id, i)
            )
        )
    await query.answer(inline_results)


@dp.callback_query_handler(text_contains= "fr-disagree")
async def revansher(call: types.CallbackQuery):
    data= call.data[3:]
    category= ''
    requirer_id= ''
    for i in data:
        try:
            n= int(i) # ...
            requirer_id+= i
        except:
            category+= i
    requirer_id= int(requirer_id)
    agreer_id= call.from_user.id    
    
    if agreer_id != requirer_id:
        first_name= call.from_user.first_name
        username= call.from_user.username
        msg= f"❌ <a href='https://t.me/{username}'>{first_name}</a> taklifni rad qildi!"
        await dp.bot.edit_message_text(
            inline_message_id= call.inline_message_id,
            text= msg,
            disable_web_page_preview=True)
    
    elif agreer_id == requirer_id:
        await call.answer('Siz o\'zingizning taklifingizni hal qila olmaysiz!😉', show_alert=True)


@dp.callback_query_handler(text_contains= "fr-")
async def revansher(call: types.CallbackQuery):
    data= call.data[3:]
    category= ''
    requirer_id= ''
    for i in data:
        try:
            n= int(i) # ...
            requirer_id+= i
        except:
            category+= i
    requirer_id= int(requirer_id)
    agreer_id= call.from_user.id

    if agreer_id!= requirer_id:
        first_name= call.from_user.first_name
        username= call.from_user.username
        try:
            msg= f"✅ <a href='https://t.me/{username}'>{first_name}</a> taklifni qabul qildi!\n👉 @temir_yolchi_bot"
            await dp.bot.send_message(
                chat_id= agreer_id, text= msg, disable_web_page_preview=True)
            await dp.bot.send_message(
                chat_id= requirer_id, text= msg, disable_web_page_preview=True)

            variant= make_variant(category)
            new_battle_id= db.new_revansh_battle(
                user1_id= agreer_id,
                user2_id= requirer_id, 
                category= category, 
                tests= variant)

            await dp.bot.edit_message_text(
                inline_message_id= call.inline_message_id, text= msg,
                disable_web_page_preview=True)

            msg= f"<b>{short_category[category]}</b><a href='https://{category}.uz'> </a> bo'yicha bellashuvni boshlash uchun quyidagi tugmani bosing.\n\nBellashuvda kim g'alaba qilsa, unga 10 💎 taqdim etiladi."
            await dp.bot.send_message(
                chat_id= requirer_id, text= msg, 
                reply_markup=start_battle_keyboard(new_battle_id),
                disable_web_page_preview=True)

            await dp.bot.send_message(
                chat_id= agreer_id, text= msg,
                reply_markup=start_battle_keyboard(new_battle_id), 
                disable_web_page_preview=True)
        except Exception as ex:
            await call.answer('Bellashuvda qatnashish uchun @temir_yolchi_bot foydalanuvchisi bo\'lishingiz zarur💁‍♂️', show_alert=True)

    elif agreer_id == requirer_id:
        await call.answer('Siz o\'zingizning taklifingiz hal qila olmaysiz!😉', show_alert=True)