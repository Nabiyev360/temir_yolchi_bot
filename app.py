import asyncio
import aioschedule
from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

async def publicate():
    users_diamonds= db.get_public_results()
    msg= ''
    n=1
    emojies= ['👨‍✈️', '🤵‍♂️', '🤵‍♂️', '👨‍🔧', '👨‍🔧', '👨‍🎓', '👨‍🎓', '👨‍🎓', '👨‍🎓', '👨‍🎓', '👨‍🎓']
    for i in users_diamonds:
        msg+= f"{n}){emojies[n-1]} {i[0]} - {i[1]} 💎\n"
        n+=1
        if n==11:
            break

    msg += f"\n@temir_yolchi_bot"
    await dp.bot.send_message(chat_id=-1001775704984, text= msg)
    
    db.clear_diamonds()

async def scheduler():
    aioschedule.every().day.at("19:00").do(publicate)           # 19+5 = 24:00 => 00:00
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(30)


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    
    db.create_table()
    
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)