#ИМПОРТ БИБЛИОТЕК
import time
import calendar
import db.db_work
from random import randint
# Скрипт для получения и обработки времени из базы данных:

def get_timely_time(what, user_id, user_name):
    if what == 'current':
        time_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        _ = time_data.split("-")
        year = int(_[0])
        month = int(_[1])
        __ = _[2].split(" ")
        day = int(__[0])
        ___ = __[1].split(":")
        h = int(___[0])
        m = int(___[1])
        s = int(___[2])
        ____, month_days = calendar.monthrange(year, month)
        year *= 3153600
        month = month_days * 86400
        day *= 86400
        h *= 3600
        m *= 60
        s += year + month + day + h + m
        return s
    elif what == 'user':
        time_data = db.db_work.get("timely_date", user_id, user_name)
        _ = time_data.split("-")
        year = int(_[0])
        month = int(_[1])
        __ = _[2].split(" ")
        day = int(__[0])
        ___ = __[1].split(":")
        h = int(___[0])
        m = int(___[1])
        s = int(___[2])
        ____, month_days = calendar.monthrange(year, month)
        year *= 3153600
        month = month_days * 86400
        day *= 86400
        h *= 3600
        m *= 60
        s += year + month + day + h + m
        return s

 # Скрипт для обновления времени получения награды для пользователя

def save_timely_time(user_id):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db.db_work.upd("timely_date", current_time, user_id)
    return 0

# Скрипт для награды пользователей
        
def timely(user, name):
    time_a = get_timely_time("user", user, name)
    time_b = get_timely_time("current", user, name)
    timely_buff = db.db_work.get("timely", user, name)
    time = time_b - time_a
    if time >= 43200:
        timely_what = "yes"
    elif time < 43200:
        timely_what = "no"
    else:
        print("ERROR: timely(): time error")
        timely_what = "no"
    if timely_what == "yes":
        balance = db.db_work.get("balance", user, name)
        level = db.db_work.get("level", user, name)
        buff = level//4
        if buff <= 1:
            buff = 1
            print("timely меньше или равно единице!")
        else:
            print("ТУТ")
        rand = int(randint(100, 120) * buff * timely_buff)
        balance = balance + rand
        save_timely_time(user)
        db.db_work.upd("balance", balance, user)
        return {"what":timely_what, "rand":rand}
    else:
        time_req = 43200 - time
        return {"what":timely_what, "time_req":time_req}