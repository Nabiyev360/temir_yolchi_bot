from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def type_keyboard(category):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('Tasodifiy raqib bilan', callback_data='with_random'))
    keyboard.add(InlineKeyboardButton('Dostim bilan', switch_inline_query=category))
    keyboard.add(InlineKeyboardButton('🔙 Orqaga', callback_data= 'to categories'))

    return keyboard



def friend_req(requirer_id, category):
    keyboard= InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(
        text= "🤝 Bellashuvga rozi bo'lish", 
        callback_data=f"fr-{category}{requirer_id}"))
    keyboard.add(InlineKeyboardButton(
        text= "🙅‍♂️ Bellashuvni rad qilish", 
        callback_data=f"fr-disagree{requirer_id}"))
    
    return keyboard   