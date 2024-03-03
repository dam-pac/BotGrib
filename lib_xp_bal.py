import db.db_work

# Скрипт увеличения валюты пользователю

def balance_up(user, amount, name):
    balance = db.db_work.get("balance", user, name)
    balance_1 = balance + amount
    if balance_1 < 0:
        return "no"
    elif balance_1 > 0:
        db.db_work.upd("balance", balance_1, user)
        return "yes"
    else:
        pass

# Скрипт для проверки нового уровня

def new_level(user, experience, name):
   level = db.db_work.get("level", user, name)
   exp = (5 * (level ** 2)) + (50 * level) + 100
   if experience >= exp:
       level += 1
       experience = experience - exp
       return {"level":level, "experience":experience, "what":"yes"}
   else:
       return {"level":level, "experience":experience, "what":"no"}

# Скрипт для получения опыта пользователем

def new_experience(user, count, name):
    experience = db.db_work.get("experience", user, name)
    experience += count
    level_check = new_level(user, experience, name)
    what = level_check.get("what")
    level = level_check.get("level")
    db.db_work.upd("level", level, user)
    experience = level_check.get("experience")
    db.db_work.upd("experience", experience, user)
    return {"what":what, "level":level}
