from aiogram.types import Message, CallbackQuery
import ast      # str to list
import asyncio

from loader import dp, db
from keyboards.inline.categories import category_keyboard
from keyboards.inline.typeKeyboard import type_keyboard
from keyboards.default.mainKeyboard import main_keyboard
from keyboards.inline.startBattleKeyboard import start_battle_keyboard
from keyboards.inline.makeVarsKeyboard import vars_maker
from keyboards.inline.revanshButton import revansher
from extra import categories, make_variant, ctgs
from data.config import ADMINS
from keyboards.inline.viewMyKeyboard import view_my_keyboard



@dp.message_handler(text= ['⚔️ Bellashuv', '/battle'])
async def battle_handler(msg: Message):
    await msg.reply('Savollar kategoriyasini tanlang:', reply_markup= category_keyboard)
    
    try:
        db.add_user(
        message.from_user.id, 
        message.from_user.first_name, 
        message.from_user.last_name, 
        message.from_user.username)
    except:
        pass

@dp.callback_query_handler(text= ctgs)
async def category_handler(call: CallbackQuery):
    for i in categories:
        if call.data==categories[i]:
            category_full_name= i
    await call.message.edit_text(
        f"<b>{category_full_name}</b><a href='https://{call.data}.uz'> </a>kategoriyasi bo'yicha kim bilan bellashmoqchisiz?",
        reply_markup= type_keyboard(call.data),
        disable_web_page_preview=True)

@dp.callback_query_handler(text= ['with_random'])
async def with_handler(call: CallbackQuery):
    await call.message.delete()
    category= call.message.entities[1].url[8:-4]
    user_id= call.from_user.id
    vs= db.check_vs_battle(category, user_id)           # None or (1, 3)
    
    for i in categories:
        if category==categories[i]:
            category_full_name = i
    
    if vs!= None:                                       # Agar bazada raqib bo'lsa
        vs_info= db.vs_battle(battle_id=vs[0], user2_id= user_id)
        battle_id= vs[0]
        await call.message.answer(
            f"<b>{category_full_name}</b><a href='https://{category}.uz'> </a>bo'yicha bellashuvni boshlash uchun quyidagi tugmani bosing.\n\nBellashuvda kim g'alaba qilsa, unga 10 💎 taqdim etiladi.",
            reply_markup=start_battle_keyboard(battle_id),
            disable_web_page_preview=True)
    else:
        variant= make_variant(category)
        new_battle_id= db.new_battle(user1_id= user_id, category= category, tests= variant)
        await call.message.answer(
            f"<b>{category_full_name}</b>\n<a href='https://{category}.uz'> </a>bo'yicha bellashuvni boshlash uchun quyidagi tugmani bosing.\n\nBellashuvda kim g'alaba qilsa, unga 10 💎 taqdim etiladi.",
            reply_markup=start_battle_keyboard(new_battle_id),
            disable_web_page_preview=True)
    
    
@dp.callback_query_handler(text_contains= 'start-')
async def battle_start_handler(call: CallbackQuery):
    category= call.message.entities[1].url[8:-4]
    battle_id= call.data[6:]

    variant= ast.literal_eval(db.get_variant(battle_id))
    
    quiz= db.get_quiz(category, quiz_id=variant[0])
    question= quiz[0]
    vars_list= [quiz[1], quiz[2], quiz[3], quiz[4]]
    quiz_photo= quiz[5]
    
    await call.message.edit_text(
        text=f"1.<a href='{quiz_photo}'> </a><b>{question}</b><a href='https://{category}.qq'> </a><a href='https://{battle_id}.qq'> </a>",
        reply_markup= vars_maker(vars_list)
)

@dp.callback_query_handler(text_contains= "ans-")
async def answer_handler(call: CallbackQuery):
    user_id= call.from_user.id
    user_ans= call.data[4:]
    quiz_number= int(call.message.text[0])
    category= call.message.entities[2].url[8:-4]
    battle_id= call.message.entities[3].url[8:-4]
    
    variant= ast.literal_eval(db.get_variant(battle_id))
    correct= db.check_answer(category, quiz_id=variant[quiz_number-1])
    
    if call.message.text[:2] != '10':
        if user_ans== correct:
            db.check_emoji(battle_id, user_id, '✅')
        elif user_ans=='bilmayman':
            db.check_emoji(battle_id, user_id, '❔')
            await call.answer(f"👳🏻‍♂️To'g'ri javob: {correct}")
        else:
            db.check_emoji(battle_id, user_id, '❌')
        
        quiz= db.get_quiz(category, quiz_id=variant[quiz_number])
        question= quiz[0]
        vars_list= [quiz[1], quiz[2], quiz[3], quiz[4]]
        quiz_photo= quiz[5]

        await call.message.edit_text(
            text= f"{quiz_number+1}.<a href='{quiz_photo}'> </a><b>{question}</b><a href='https://{category}.uz'> </a><a href='https://{battle_id}.uz'> </a>",
            reply_markup=vars_maker(vars_list))
    
    
    elif call.message.text[:2] == '10':
        quiz_number= int(call.message.text[:2])
        correct= db.check_answer(category, quiz_id=variant[quiz_number-1])
        
        if user_ans== correct:
            db.check_emoji(battle_id, user_id, '✅')
        elif user_ans=='bilmayman':
            db.check_emoji(battle_id, user_id, '❔')
            await call.answer(f"👳🏻‍♂️To'g'ri javob: {correct}")
        else:
            db.check_emoji(battle_id, user_id, '❌')
            
        try:
            await call.message.delete()
        except:
            pass
        
        overall= db.overall_result(battle_id)
        
        if overall[1] != None and overall[3] != None:
            try:    # ko'p xatolik chiqqanligi uchun tryga oldim
                if len(overall[1]) >= 10 and len(overall[3]) >= 10:
                    user_1_info= db.get_user(user_id=overall[0])
                    fullname1= user_1_info[1] #+ user_1_info[2]
                    username1= user_1_info[3]
                    
                    
                    user_2_info= db.get_user(user_id=overall[2])
                    fullname2= user_2_info[1] #+ user_2_info[2]
                    username2= user_2_info[3]
                    
                    corrects_count1= overall[1][:10].count('✅')
                    corrects_count2= overall[3][:10].count('✅')
                    
                    for i in categories:
                        if categories[i]==category:
                            category_msg =i
                    
                    msg= ''
                    msg+= f"<b>{category_msg}</b> bo'yicha o'tkazilgan bellashuv natijalari" + '\n\n'
                    
                    if corrects_count1 > corrects_count2:
                        msg+= f"<a href= 'https://t.me/{username1}'>{fullname1}</a>: 👑 {corrects_count1}/10 | +10💎\n"
                        msg+= f"<a href= 'https://t.me/{username2}'>{fullname2}</a>: 😭 {corrects_count2}/10 \n\n"
                        msg+= '👑 | ' + overall[1][:10] +'\n'
                        msg+= '😭 | ' + overall[3][:10]
                        db.update_diamond(overall[0])
                    
                    elif corrects_count1 < corrects_count2: 
                        msg+= f"<a href= 'https://t.me/{username2}'>{fullname2}</a>: 👑 {corrects_count2}/10 | +10💎\n"
                        msg+= f"<a href= 'https://t.me/{username1}'>{fullname1}</a>: 😭 {corrects_count1}/10 \n\n"
                        msg+= '👑 | ' + overall[3][:10] +'\n'
                        msg+= '😭 | ' + overall[1][:10]
                        db.update_diamond(overall[2])
                    
                    else:
                        msg+= f"<a href= 'https://t.me/{username1}'>{fullname1}</a>: 🤝 {corrects_count1}/10 | +{corrects_count1}💎\n"
                        msg+= f"<a href= 'https://t.me/{username2}'>{fullname2}</a>: 🤝 {corrects_count2}/10 | +{corrects_count2}💎\n\n"
                        msg+= '🤝 | ' + overall[1][:10] +'\n'
                        msg+= '🤝 | ' + overall[3][:10]
                        db.update_diamond_be_equal(overall[0], corrects_count1)
                        db.update_diamond_be_equal(overall[2], corrects_count2)
                    
                    markup1= revansher(overall[2], category)
                    markup2= revansher(overall[0], category)
                    
                    await dp.bot.send_message(chat_id= overall[0], text= msg, disable_web_page_preview=True, reply_markup=markup1)
                    await dp.bot.send_message(chat_id= overall[2], text= msg, disable_web_page_preview=True, reply_markup=markup2)
                else:
                    await call.message.answer("Raqib bellashuvni yakunlagani yo'q. Kutib turing bellashuv yakunlanishi bilan natijalarni sizga yuboramiz. \nO'z natijangizni hoziroq bilish uchun tugmani bosing👇",
                    reply_markup=view_my_keyboard(battle_id))
            except Exception as ex:
                await dp.bot.send_message(chat_id= ADMINS[0], text= f"User 1: {user_1_info}\nUser 2: {user_2_info}")
                await asyncio.sleep(0.5)
                await dp.bot.send_message(chat_id= ADMINS[0], text=ex)

        else:   
            await call.message.answer("Raqib bellashuvni yakunlagani yo'q. Kutib turing bellashuv yakunlanishi bilan natijalarni sizga yuboramiz. \nO'z natijangizni hoziroq bilish uchun tugmani bosing👇", 
            reply_markup=view_my_keyboard(battle_id))