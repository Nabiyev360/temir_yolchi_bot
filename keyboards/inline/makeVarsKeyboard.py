from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randrange

def vars_maker(vars_list):
    keyboard= InlineKeyboardMarkup(row_width=2)

    short = True
    for var in vars_list:
        if var != None:
            if len(var) >= 20:
                short = False


    while vars_list:
        rand_idx= randrange(len(vars_list))
        rand_var= vars_list[rand_idx]
        if rand_var != None:
            if short:
                keyboard.insert(InlineKeyboardButton(rand_var, callback_data='ans-'+rand_var))
            else:
                keyboard.add(InlineKeyboardButton(rand_var, callback_data='ans-'+rand_var))
        vars_list.remove(rand_var)
    keyboard.add(InlineKeyboardButton('Bilmayman 🏳️', callback_data='ans-bilmayman'))
    return keyboard