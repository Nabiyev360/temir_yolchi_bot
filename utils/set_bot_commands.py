from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("battle", "Yangi bellashuv"),
            types.BotCommand("reyting", "Foydalanuvchilar reytingi"),
            # types.BotCommand("help", "Yo'riqnoma")
        ]
    )