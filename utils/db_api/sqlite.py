import sqlite3

path_to_quiz_db= 'data/quiz.db'
path_to_battles_db= 'data/battles.db'
path_to_users_db= 'data/users.db'

def create_table():
    for i in ['ltl', "iyod", "lej", "hxtt", 'ltxk']:
        conn = sqlite3.connect(path_to_quiz_db)
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {i}(\
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,\
            question TEXT NOT NULL,\
            variant_1 TEXT, \
            variant_2 TEXT,\
            variant_3 TEXT,\
            answer TEXT,\
            manba TEXT,\
            quiz_photo TEXT DEFAULT NULL\
        )")
        conn.commit()
   
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS battles(\
        battle_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        user1_id INTEGER,\
        user2_id INTEGER,\
        category TEXT,\
        tests TEXT,\
        result_1 TEXT,\
        result_2 TEXT,\
        count_1 INTEGER,\
        count_2 INTEGER\
    )")
    conn.commit()
    conn.close()

    conn = sqlite3.connect(path_to_users_db)
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS users(\
        user_id INTEGER PRIMARY KEY,\
        first_name TEXT,\
        last_name TEXT,\
        username TEXT,\
        nickname TEXT,\
        course TEXT,\
        region TEXT,\
        diamond INTEGER DEFAULT 0,\
        energy INTEGER DEFAULT 0\
    )")
    conn.commit()
    conn.close()

# BATTLES DB
def check_vs_battle(category, user_id):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"SELECT battle_id, user1_id, category, tests FROM battles \
        WHERE user2_id IS NULL AND category= '{category}' AND user1_id != '{user_id}'")
    battle= cur.fetchone()
    return battle

def vs_battle(battle_id, user2_id):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"UPDATE battles\
        SET user2_id= {user2_id} WHERE battle_id= {battle_id}")
    conn.commit()
    conn.close()

def new_battle(user1_id, category, tests):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO battles(user1_id, category, tests)\
        VALUES({user1_id}, '{category}', '{tests}')")
    conn.commit()
    cur.execute(f"SELECT COUNT(battle_id) FROM battles")
    last_battle_id = cur.fetchone()[0]
    conn.close()
    return last_battle_id

def new_revansh_battle(user1_id, user2_id, category, tests):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO battles(user1_id, user2_id, category, tests)\
        VALUES({user1_id}, {user2_id}, '{category}', '{tests}')")
    conn.commit()
    cur.execute(f"SELECT COUNT(battle_id) FROM battles")
    last_battle_id = cur.fetchone()[0]
    conn.close()
    return last_battle_id
    
def get_quiz(category, quiz_id):
    conn = sqlite3.connect(path_to_quiz_db)
    cur = conn.cursor()
    cur.execute(f"SELECT question, variant_1, variant_2, variant_3, answer, quiz_photo FROM {category} WHERE quiz_id= {quiz_id}")
    vars= cur.fetchone()
    return vars

def check_answer(category, quiz_id):
    conn = sqlite3.connect(path_to_quiz_db)
    cur = conn.cursor()
    cur.execute(f"SELECT answer FROM {category} WHERE quiz_id= {quiz_id}")
    vars= cur.fetchone()[0]
    return vars
    
def quiz_count(category):
    conn = sqlite3.connect(path_to_quiz_db)
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(quiz_id) FROM {category}")
    count = cur.fetchone()[0]
    return count

def get_variant(battle_id):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"SELECT tests FROM battles WHERE battle_id= {battle_id}")
    variant = cur.fetchone()[0]
    return variant
    
def check_emoji(battle_id, user_id, symbol):
    conn = sqlite3.connect(path_to_battles_db)
    cur = conn.cursor()
    cur.execute(f"SELECT user1_id, user2_id FROM battles WHERE battle_id= {battle_id}")
    players= cur.fetchone()
    user1_id= players[0]
    user2_id= players[1]
    
    if user_id== user1_id:
        cur.execute(f"SELECT result_1 FROM battles WHERE battle_id= {battle_id}")
        result_1= cur.fetchone()[0]
        if result_1 == None:
            result_1= ''
        next_result= result_1+ symbol
        cur.execute(f"UPDATE battles SET result_1= '{next_result}' WHERE battle_id= {battle_id}")
    
    elif user_id== user2_id:
        cur.execute(f"SELECT result_2 FROM battles WHERE battle_id= {battle_id}")
        result_2= cur.fetchone()[0]
        if result_2 == None:
            result_2= ''
        next_result= result_2+ symbol
        cur.execute(f"UPDATE battles SET result_2= '{next_result}' WHERE battle_id= {battle_id}")
    conn.commit()
    conn.close()
    
def overall_result(battle_id):
    conn= sqlite3.connect(path_to_battles_db)
    cur= conn.cursor()
    cur.execute(f"SELECT user1_id, result_1, user2_id, result_2 FROM battles WHERE battle_id= {battle_id}")
    overall= cur.fetchone()
    return overall



# USERS DB
def add_user(user_id, first_name, last_name= '', username= None):
    conn= sqlite3.connect(path_to_users_db)
    cur= conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if not cur.fetchone():
        cur.execute(f"INSERT INTO users(user_id, first_name, last_name, username) \
            VALUES ({user_id}, '{first_name}', '{last_name}', '{username}')")
        conn.commit()
    else:
        pass    # UPDATE yozish kerak
    conn.close()

def get_user(user_id):
    conn= sqlite3.connect(path_to_users_db)
    cur= conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id= {user_id}")
    overall= cur.fetchone()
    return overall

def update_diamond(user_id):
    conn = sqlite3.connect(path_to_users_db)
    cur = conn.cursor()
    cur.execute(f"SELECT diamond FROM users WHERE user_id= {user_id}")
    user_diamonds= cur.fetchone()[0]
    cur.execute(f"UPDATE users SET diamond= {user_diamonds +10} WHERE user_id= {user_id}")
    conn.commit()
    conn.close()
    
def update_diamond_be_equal(user_id, count):
    conn = sqlite3.connect(path_to_users_db)
    cur = conn.cursor()
    cur.execute(f"SELECT diamond FROM users WHERE user_id= {user_id}")
    user_diamonds= cur.fetchone()[0]
    cur.execute(f"UPDATE users SET diamond= {user_diamonds + count} WHERE user_id= {user_id}")
    conn.commit()
    conn.close()
    
def get_diamonds_stat(user_id):
    conn = sqlite3.connect(path_to_users_db)
    cur = conn.cursor()
    cur.execute(f"SELECT first_name, diamond FROM users ORDER BY diamond DESC LIMIT 10")
    diamonds_stat= cur.fetchall()
    cur.execute(f"SELECT first_name, diamond FROM users WHERE user_id= {user_id}")
    diamonds_stat.append(cur.fetchone())
    cur.execute(f"SELECT diamond FROM users")
    all= cur.fetchall()
    return diamonds_stat, all   
    

def get_public_results():
    conn = sqlite3.connect(path_to_users_db)
    cur = conn.cursor()
    cur.execute(f"SELECT first_name, diamond FROM users ORDER BY diamond DESC LIMIT 10")
    diamonds_stat= cur.fetchall()
    return diamonds_stat
    

def get_users_id():
    conn = sqlite3.connect(path_to_users_db)
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM users")
    sender_id = c.fetchall()
    return sender_id


def count_users():
    conn = sqlite3.connect(path_to_users_db)
    c = conn.cursor()
    c.execute(f"SELECT COUNT() FROM users")
    count = c.fetchone()[0]
    return count

def clear_diamonds():
    conn = sqlite3.connect(path_to_users_db)
    c = conn.cursor()
    c.execute(f"UPDATE users SET diamond=0")
    conn.commit()
    conn.close()

def get_my_result(battle_id, user_id):
    conn = sqlite3.connect(path_to_battles_db)
    c = conn.cursor()
    c.execute(f"SELECT * FROM battles WHERE battle_id={battle_id} AND (user1_id= {user_id} OR user2_id= {user_id})")
    res = c.fetchone()
    return res