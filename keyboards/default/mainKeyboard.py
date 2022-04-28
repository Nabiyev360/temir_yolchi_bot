from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('⚔️ Bellashuv')
        ],
        [
           # KeyboardButton('🤓 Mashqlar'),
            KeyboardButton('📊 Reyting'),
            # KeyboardButton("📜 Qo'llanma")
        ],
       # [
            # KeyboardButton("📜 Qo'llanma"),
    #         KeyboardButton("🔧 Sozlamalar")

        # ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)