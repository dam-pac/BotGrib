import sqlite3

def get(what, user_id, user_name="test"):
    """
        get:
            user_name
            experience
            level
            balance
            timely_date
            lives
            timely
            exp_buff
            kurs
    """
    connect = sqlite3.connect("db\\data.db")
    cursor = connect.cursor()
    cursor.execute(''' SELECT {} FROM data WHERE user_id = ?'''.format(what), (user_id,))
    data = cursor.fetchone()
    connect.close()
    if data == None:
        add(user_id, user_name)
        connect = sqlite3.connect("db\\data.db")
        cursor = connect.cursor()
        cursor.execute(''' SELECT {} FROM data WHERE user_id = ?'''.format(what), (user_id,))
        data = cursor.fetchone()
        connect.close()
    return data[0]
def add(user_id, user_name, experience=0, level=1, balance=0, timely_date="2024-02-1 00:00:00", lives=100, timely=1.0, exp_buff=1.0, kurs=0.7):
    """
    add:
        user_id
        user_name
        experience
        level
        balance
        timely_date
        lives
        timely
        exp_buff
        kurs
    """
    connect = sqlite3.connect("db\\data.db")
    cursor = connect.cursor()
    cursor.execute('INSERT INTO data (user_id, user_name, experience, level, balance, timely_date, lives, timely, exp_buff, kurs) VALUES (?,?,?,?,?,?,?,?,?,?)', (user_id, user_name, experience, level, balance, timely_date, lives, timely, exp_buff, kurs,))
    connect.commit()
    connect.close()
    return 0
def upd(what, value, user_id):
    connect = sqlite3.connect('db\\data.db')
    cursor = connect.cursor()
    cursor.execute('UPDATE data SET {} = ? WHERE user_id = ?'.format(what), (value, user_id))
    connect.commit()
    connect.close()
    return 0
def get_column(what):
    connect = sqlite3.connect("db\\data.db")
    cursor = connect.cursor()
    cursor.execute('SELECT {} FROM data'.format(what))
    return cursor.fetchall()