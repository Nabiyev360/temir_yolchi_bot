from aiogram import types

from loader import dp, db
from keyboards.default.mainKeyboard import main_keyboard

@dp.message_handler(text= ['📊 Reyting', '/reyting'])
async def send_statistics(message: types.Message):
    name= message.from_user.first_name
    diamonds_stat= db.get_diamonds_stat(message.from_user.id)
    users_diamonds= diamonds_stat[0]

    msg= ''
    n=1
    for i in users_diamonds:
        msg+= f"{n})👤 {i[0]} - {i[1]} 💎\n"
        n+=1
        if n==11:
            break
    
    all= []
    for d in diamonds_stat[1]:
        all.append(d[0])
    all.sort(reverse=True)

    if users_diamonds[-1][1] == 0:
        user_place= db.count_users()
    else:
        user_place= all.index(users_diamonds[-1][1]) + 1

    msg+=f"...\n{user_place})👤 {name} - {users_diamonds[-1][1]} 💎"
    msg+=f"\n<b>Kunlik natijalar - @temir_yolchi_public</b>"
    
    await message.answer(msg, reply_markup=main_keyboard)