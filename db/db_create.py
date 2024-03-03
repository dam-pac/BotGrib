import sqlite3

def create():
    '''        
        user_name
        experience
        level
        balance
        timely_date
        lives
        timely
        exp_buff
        kurs
    '''
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,               
    user_name TEXT NOT NULL,
    experience INTEGER DEFAULT (0),
    level INTEGER DEFAULT (0),
    balance INTEGER DEFAULT (0),
    timely_date TEXT DEFAULT "0",
    lives REAL DEFAULT (100),
    timely REAL DEFAULT (1.0),
    exp_buff REAL DEFAULT (1.0),
    kurs REAL DEFAULT (0.7)               
    )
    ''')

    connection.commit()
    connection.close()
    return 0
    #