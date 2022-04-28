from random import randrange

from loader import db
from utils.db_api.sqlite import quiz_count


ctgs = ['ltl', "iyod", "lej", "hxtt", 'ltxk']

short_category= {
    'ltl':'Lokomotivlar tuzilishi va loyihalash', 
    'iyod':'Ichki yonuv dvigatelleri',
    'lej':'Lokomotiv elektr jihozlari', 
    'hxtt':'Harakat xavfsizligi va tormoz tizimlari', 
    'ltxk':"Texnik xizmat ko'rsatish va diaginostika"}

categories= {
    'Lokomotivlar tuzilishi va loyihalash':'ltl', 
    'Ichki yonuv dvigatelleri':'iyod', 
    'Lokomotiv elektr jihozlari':'lej', 
    'Harakat xavfsizligi va tormoz tizimlari':'hxtt', 
    "Texnik xizmat ko'rsatish va diaginostika":'ltxk'}



def make_variant(category):
    variant= []
    quiz_count= db.quiz_count(category)
    
    while len(variant)<10:
        random_id= randrange(1, quiz_count+1)
        if random_id not in variant:
            variant.append(random_id)
    
    return variant