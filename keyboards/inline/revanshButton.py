from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def revansher(enemy_id, category):
    button= InlineKeyboardMarkup().add(
        InlineKeyboardButton('👊 Revansh', 
        callback_data=f"{enemy_id}, '{category}'"))
    return button
    
def revansh_req(requirer_id):
    req_keyboard= InlineKeyboardMarkup()
    req_keyboard.add(
        InlineKeyboardButton(text= "🤝 Bellashuvga rozi bo'lish", 
        callback_data=f're-agree-{requirer_id}'))
    req_keyboard.add(
        InlineKeyboardButton(text= "🙅‍♂️ Bellashuvni rad qilish",
        callback_data=f'disagree-{requirer_id}'))
    return req_keyboard