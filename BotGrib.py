 # -*- coding: utf-8 -*-
#Загрузка библиотек
from ast import Delete
from calendar import month
import disnake
from disnake import Option
from disnake.ext import commands
from disnake.embeds import Embed
from datetime import datetime
from random import randint
import math
import asyncio
import os
import db.db_create
import db.db_work
from lib_timely import *
from lib_xp_bal import *
#!МЕСТО ДЛЯ ТОКЕНА БОТА!
token = ""

emoji_perl = "<:perl:1167865266479321209>"
version = "0.2.1.DATA_BASE"





# Начало кода бота
    #Инициализация бота
intents = disnake.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
    #Вывод сообщения об успешном входе
@bot.event
async def on_ready():
    print(f'Бот вошёл в дискорд под именем {bot.user.name}.')


@bot.slash_command(name='user', description='Показать всю информацию о пользователе!')
async def user(ctx, пользователя: disnake.Member):
    user = пользователя
    user_name = user.name
    user_id = user.id
    experience = db.db_work.get("experience", user_id, user_name)
    level = db.db_work.get("level", user_id, user_name)
    balance = db.db_work.get("balance", user_id, user_name)
    timely = db.db_work.get("timely", user_id, user_name)
    exp_buff = db.db_work.get("exp_buff", user_id, user_name)
    kurs = db.db_work.get("kurs", user_id, user_name)
    lives = db.db_work.get("lives", user_id, user_name)
    level_req = (5 * (level ** 2)) + (50 * level) + 100
    req = level_req - experience
    exp = experience
    _ = level_req / 20
    __ = _ / 2
    poln = 0
    pol = 0
    pus = 0
    sin_1 = '█'
    sin_2 = '▓'
    sin_3 = '░'
    for i in range(1, 21):
        if exp >= _:
            poln += 1
            exp -= _
        elif exp < _ and exp > 0:
            pol += 1
            exp -= __
        else:
            pus += 1
    level_shkala = sin_1 * poln + sin_2 * pol + sin_3 * pus

    embed = Embed(title=f':information_source: Информация о {user_name}', description=f'', color=disnake.Color.blue())
    embed.set_author(
    name=f"Запущено {ctx.user.name}",
    icon_url=f"{ctx.user.avatar}",
)
    embed.set_footer(
    text=f"Бот {bot.user.name}",
    icon_url=f"{bot.user.avatar}",
)
    embed.set_thumbnail(url=f"{user.avatar}")
    embed.add_field(name=f"**                        УРОВЕНЬ\n                           -- {level} --**", value=f"", inline=False)
    embed.add_field(name="Шкала уровня", value=f"{level_shkala}\n :star: {experience} из {level_req} опыта | {req} --> {level+1} уровень", inline=False)
    embed.add_field(name="Баланс", value=f"{emoji_perl} {balance}", inline=True)
    embed.add_field(name="Опыт", value=f":star: {experience}", inline=True)
    embed.add_field(name="Множитель награды", value=f":sparkles: {timely}", inline=True)
    embed.add_field(name="Множитель опыта", value=f":sparkles: {exp_buff}", inline=True)
    embed.add_field(name="Множитель курса обмена", value=f":sparkles: {kurs}", inline=True)
    embed.add_field(name="Количество жизней", value=f":heart:{lives}", inline=True)
    await ctx.send(embed=embed)

    #Код бота для запуска скрипта добавления опыта за сообщение

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if not message.author.bot:
        if message.channel.id == 1095600257896812554 or message.channel.id == 1208159489803558953:
            pass
        else:
            exp_buff = db.db_work.get("exp_buff", message.author.id, message.author.name)
            amount = 1 * exp_buff
            add_exp = new_experience(message.author.id, amount, message.author.name)
            what = add_exp.get("what")
            level = add_exp.get("level")
            if what == "no":
                pass
            elif what == "yes":
                print(f"LEVEL_UP: {message.author.id}")
                embed = Embed(title=f'· · • {level} • · ·', description=f':star2: Оп! {message.author.mention} Твой LV вырос!', color=disnake.Color.blue())
                await message.channel.send(embed=embed)
            else:
                pass
    else:
        message_list = message.content.split(" ")
        if message_list[0] == "!trans":
            msg = await message.channel.send(f"{message.author.mention} Данные получены! Обработка...")
            try:
                user_id = message_list[1]
                balance = int(message_list[2])
                level = int(message_list[3])
                experience = int(message_list[4])
                user_name = str(message_list[5])
                user_id_db = db.db_work.get("user_id", user_id, user_name)
                user_name_db = db.db_work.get("user_name", user_id, user_name)
                if user_name_db == user_name or user_id_db == user_id:
                    db.db_work.upd("user_name", user_name, user_id)
                    db.db_work.upd("user_id", user_id, user_id)
                    db.db_work.upd("balance", balance, user_id)
                    db.db_work.upd("level", level, user_id)
                    db.db_work.upd("experience", experience, user_id)
                else:
                    db.db_work.add(user_id, user_name, experience, level, balance)
                await msg.edit(f":white_check_mark: Данные успешно обработаны!")
            except:
                await msg.edit(f':x: Обработка не удалась')
        else:
            pass

    #Код слэш команды для показа ранка пользователей

@bot.slash_command(name='rank', description='Показать свой ранг')
async def rank(ctx, пользователя: disnake.Member):
    user = пользователя
    level = db.db_work.get("level", user.id, user.name)
    exp = (5 * (level ** 2)) + (50 * level) + 100
    experience = db.db_work.get("experience", user.id, user.name)
    embed = disnake.Embed(
    title="· · • Ранг • · ·",
    description=f" Ваш уровень: {level} | Ваш опыт: {experience} => {exp}",
    colour=disnake.Color.blurple(),
    )
    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar}")
    await ctx.send(embed=embed)

    #Код слэш команды для получения награды пользователем

@bot.slash_command(name='timely', description='Получи награду timely!')
async def timely_claim(inter: disnake.ApplicationCommandInteraction):
    user = inter.author.id
    name = inter.author.name
    timely_list = timely(user, name)
    what = timely_list.get("what")
    if what == 'no':
        time_req = int(timely_list.get("time_req"))
        if time_req < 60:
            embed = Embed(title='', description=f':stopwatch: {inter.author.mention} Вы достигли кулдауна этой команды. Вы сможете использовать её вновь через {time_req} секунд!', color=disnake.Color.red())
            await inter.response.send_message(embed=embed)
        elif time_req >= 60:
            time_req_m = time_req/60
            time_req_m_round = int(time_req_m)
            time_req_s = int((time_req_m - time_req_m_round) * 60)
            if time_req_m >= 60:
                time_req_h = time_req_m/60
                time_req_m = int((time_req_h - int(time_req_h)) * 60)
                time_req_h = int(time_req_h)
                embed = Embed(title='', description=f':stopwatch: {inter.author.mention} Вы достигли кулдауна этой команды. Вы сможете использовать её вновь через {int(time_req_h)} ч. {int(time_req_m)} м. {int(time_req_s)} с.!', color=disnake.Color.red())
                await inter.response.send_message(embed=embed)
            else:
                embed = Embed(title='', description=f':stopwatch: {inter.author.mention} Вы достигли кулдауна этой команды. Вы сможете использовать её вновь через {int(time_req_m)} м. {int(time_req_s)} с.!', color=disnake.Color.red())
                await inter.response.send_message(embed=embed)
        else:
            pass
    elif what == 'yes':
        rand = timely_list.get("rand")
        lives = db.db_work.get("lives", user, name)
        if lives > 80:
            lives = 100
        elif lives <= 80:
            lives += 20
        db.db_work.upd("lives", user, name)
        embed = Embed(title=f'', description=f'', color=disnake.Color.blue())
        embed.add_field(name=f"Ваша ежедневная награда! {rand} {str(emoji_perl)} Блёбопёрлов", value="", inline=False)
        embed.set_author(name=f" {inter.author.name}", icon_url=f"{inter.author.avatar}")
        embed.set_footer(text=f" {inter.author.name} Вы получили 20 жизней **↑{lives}↑**")        

        button1 = disnake.ui.Button(label=":bell: Уведомить меня", style=disnake.ButtonStyle.primary, custom_id="timely_remind")
        await inter.response.defer()
        await inter.followup.send(embed=embed)
    else:
        print("ERROR: timely(): timely error, argument what != yes or no!")
        await inter.send("ERROR: timely(): timely error, argument what != yes or no!")

    #Код слэш команды для очистки чата

@bot.slash_command(name='clear', description = 'Удалить сообщения')
@commands.default_member_permissions(manage_messages=True)
async def clear_messages(ctx, сколько_сообщений: int):
    messages = сколько_сообщений
    if messages >= 1 and messages <= 100:
        await ctx.channel.purge(limit=messages)
        embed = disnake.Embed(title="", description=f":white_check_mark: Команда успешно выполнена! Было очищено {messages} сообщений", colour=disnake.Color.blue())
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.delete_original_message()
    else:
        embed = disnake.Embed(title="", description=f":x: Можно удалить только до 100 сообщений", colour=disnake.Color.blue())
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.delete_original_message()

    #Код слэш команды для просмотра баланса

@bot.slash_command(name='balance', description='Посмотреть баланс')
async def balance(ctx, пользователя:disnake.Member):
    user = пользователя
    balance = db.db_work.get("balance", user.id, user.name)
    embed = disnake.Embed(title="", description=f"У тебя {balance} {str(emoji_perl)} Блёбопёрлов, блёп-блёп..", colour=disnake.Color.blue())
    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar}")
    await ctx.response.defer()
    await ctx.followup.send(embed=embed)
    
    #Код слэш команды для увеличения баланса пользователей

@bot.slash_command(name='gift', description='Увеличение баланса для пользователей {опасно}')
@commands.has_role('Гриб')
async def gift(ctx, сколько: int, кому:disnake.Member):
    amount = сколько
    user_ = кому
    print(f"Info: gift command: Пользователь {ctx.author.name} запустив команду передал пользователю {user_.name} {amount} Блёбопёрлов")
    name = ctx.author.name
    what = balance_up(user_.id, amount, name)
    if what == 'no':
        embed = disnake.Embed(title="", description=f":x: {ctx.author.mention} Недопустим отрицательный баланс для пользователей", colour=disnake.Color.blue())
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.delete_original_message()
    elif what == 'yes':
        embed = disnake.Embed(title="", description=f":white_check_mark: Команда успешно выполнена!", colour=disnake.Color.blue())
        await ctx.send(embed=embed)
    else:
        pass
    
    #Команда для передачи валюты между пользователями

@bot.slash_command(name='give', description='Передать валюту пользователю')
async def give(inter: disnake.ApplicationCommandInteraction, сколько: int, кому:disnake.Member):
    #print(f"Info: gift command: Пользователь {ctx.author.name} запустив команду передал пользователю {user_.name} {amount} Блёбопёрлов")
    amount = сколько
    user_ = кому
    if amount >= 10:
        name = inter.author.name
        what = balance_up(inter.author.id, -amount, name)
        if what == 'yes':
            name = user_.name
            what = balance_up(user_.id, amount, name)
            embed = disnake.Embed(title="", description=f":white_check_mark: {inter.author.mention} успешно перевёл {amount} {str(emoji_perl)} пользователю {user_.mention}", colour=disnake.Color.blue())
            embed.set_author(name=f"{inter.author.name}", icon_url=f"{inter.author.avatar}")
            await inter.send(embed=embed)
        elif what == 'no':
            balance = db.db_work.get("balance", inter.author.id, name)
            embed = disnake.Embed(title="", description=f":x: {inter.author.mention} Вы не можете отправить {amount} {str(emoji_perl)} \n Пожалуйста, введите значение не более вашего баланса: {balance} {str(emoji_perl)}", colour=disnake.Color.red())
            message = await inter.send(embed=embed)
            await asyncio.sleep(5)
            await inter.delete_original_message()
        else:
            print("Ошибка команды передачи валюты")
    else:
        embed = disnake.Embed(title="", description=f"{inter.author.mention} :x: Вы не можете отправить менее 10 {str(emoji_perl)}", colour=disnake.Color.red())
        message = await inter.send(embed=embed)
        await asyncio.sleep(5)
        await inter.delete_original_message()
    


@bot.slash_command(name='wheel', description='Поиграть на удачу в казино!')
async def wheel(ctx, сколько: int):
    amount_1 = сколько
    if amount_1 >= 10:
        balance = db.db_work.get("balance", ctx.user.id, ctx.user.name)
        if balance >= amount_1:
            name = ctx.author.name
            what = balance_up(ctx.user.id, -amount_1, name)
            rand = randint(1,8)
            if rand == 1:
                k = 2.4
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣**x2.4** \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.green())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 2:
                k = 1.7
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣**x1.7** \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.green())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 3:
                k = 1.5
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣**x1.5** \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.green())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 4:
                k = 1.2
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣**x1.2** \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.orange())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 5:
                k = 0.5
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣**x0.5** \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.orange())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 6:
                k = 0.3
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣**x0.3** \n ╠══╣||x0.2|| \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.red())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 7:
                k = 0.2
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣**x0.2** \n ╠══╣||x0.1|| \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.red())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            elif rand == 8:
                k = 0.1
                amount = math.ceil(amount_1 * k)
                what = balance_up(ctx.user.id, amount, name)
                embed = disnake.Embed(title="", description=f" ╠══╣||x2.4|| \n ╠══╣||x1.7|| \n ╠══╣||x1.5|| \n ╠══╣||x1.2|| \n\n ╠══╣||x0.5|| \n ╠══╣||x0.3|| \n ╠══╣||x0.2|| \n ╠══╣**x0.1** \n\n Модификатор: \n {k}x \n\n Выиграл: \n {amount} {str(emoji_perl)}", colour=disnake.Color.red())
                embed.set_author(name=f"{ctx.user.name} поставил {amount_1} блёбопёрлов", icon_url=f"{ctx.user.avatar}")
                await ctx.send(embed=embed)
            else:
                print("Ошибка рандома в рулетке!")
        else:
            embed = disnake.Embed(title="", description=f":x: {ctx.author.mention} Вы не можете поставить более значения вашего баланса, пожалуйста, введите более 10 {str(emoji_perl)} или менее {balance} {str(emoji_perl)} Блёбопёрлов", colour=disnake.Color.red())
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await ctx.delete_original_message()
    else:
        embed = disnake.Embed(title="", description=f":x: {ctx.author.mention} Вы не можете поставить менее 10 {str(emoji_perl)}", colour=disnake.Color.red())
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.delete_original_message()
    #Код команды ЭХО

@bot.slash_command(name="top", description="Показать топ пользователей!")
async def top(ctx):
    level_data = db.db_work.get_column("level")
    id_users = db.db_work.get_column("user_id")
    experience = db.db_work.get_column("experience")
    total_data = {}
    _ = 0
    __ = []
    ___ = []
    for item in id_users:
        __.append(item[0])
    for item in experience:
        ___.append(item[0])
    for item in level_data:
        experience = 0
        for i in range(0, item[0]):
            if i == 0:
                pass
            else:
                experience += (5 * (i ** 2)) + (50 * i) + 100
        id_user = __[_]
        experience += ___[_]
        total_data[id_user] = experience
        _ += 1
    amount = len(id_users)
    embed = disnake.Embed(title=":trophy: Топ рейтинга участников", description=f"", colour=disnake.Color.blue())
    dick_sort = sorted(total_data.items(), key=lambda item: item[1], reverse=True)
    for i in range(0, amount-1):
        dick_tuple = dick_sort[i]
        user_id = dick_tuple[0]
        level = db.db_work.get("level", user_id)
        experience = db.db_work.get("experience", user_id)
        user_name = db.db_work.get("user_name", user_id)
        print(user_id)
        print(dick_tuple)
        if i <= 15:
            if i+1 == 1:
                pass
                embed.add_field(name=f":first_place: #{i+1}. {user_name}", value=f"**Уровень:** {level} | **Опыт:** {experience}", inline=False)
            elif i+1 == 2:
                pass
                embed.add_field(name=f":second_place: #{i+1}. {user_name}", value=f"**Уровень:** {level} | **Опыт:** {experience}", inline=False)
            elif i+1 == 3:
                pass
                embed.add_field(name=f":third_place: #{i+1}. {user_name}", value=f"**Уровень:** {level} | **Опыт:** {experience}", inline=False)
            else:
                pass
                embed.add_field(name=f" #{i+1}. {user_name}", value=f"**Уровень:** {level} | **Опыт:** {experience}", inline=False)
    embed.set_footer(text=f"Запросил {ctx.user.name}")
    await ctx.send(embed=embed)





   #

    #Слэш команда для показа списка доступных команд

@bot.slash_command(name='cmds', description='Список команд')
async def cmds(ctx):
    embed = disnake.Embed(title="Список доступных команд", description=f"  !===> Будь осторожен <===! ", colour=disnake.Color.green())
    embed.add_field(name=f"  => cmds", value=f"Ты запустил эту команду. Показывает список доступных моих команд", inline=False)
    embed.add_field(name=f"  => top", value=f"Показывает ТОП 15 пользователей по уровню. Стань самым первым!", inline=False)
    embed.add_field(name="  => balance {пользователя}", value=f"Показывает количество ваших средств. Наверное пора их потратить?", inline=False)
    embed.add_field(name="  => rank {пользователь}", value=f"Помогает узнать ваш уровень и сколько нужно для следующего", inline=False)
    embed.add_field(name=f"  => user", value=f"Показывает полную информацию о вас, что знает бот", inline=False)
    embed.add_field(name=f"  => timely", value=f"Позволяет получить награду! Совершенно бесплатно)", inline=False)
    embed.add_field(name="  => wheel {количество средств}", value=f"Попробуй испытать удачу в настоящей рулетке", inline=False)
    embed.add_field(name="  => walk", value=f"Стоит сходить прогуляться на улицу, а может и найти пару плюшек (=^･ω･^=)", inline=False)
    embed.add_field(name="  => give {количество} {пользователь}", value=f"Передаёт ваши средства другому пользователю. Он явно будет вам рад", inline=False)
    embed.add_field(name="  [MODERS] => clear {количество}", value=f"Очистить чат и оставить всё в прошлом", inline=False)
    embed.add_field(name="  [ADMINS] => !gift {количество} {пользователь}", value=f"Добавить или забрать валюту у пользователя", inline=False)
    embed.add_field(name=f"  [ADMINS] => edit", value=f"Изменить значение у пользователя в базе данных", inline=False)
    embed.add_field(name=f"  [ADMINS] => add", value=f"Создать и добавить дового пользователя со всеми аттрибутами (скоро)", inline=False)
    embed.add_field(name="  [BOTS] => !trans", value=f"Передача данных", inline=False)
    embed.add_field(name=f"  [TECH] => stop", value=f"Выключить бота, закрыть программу (скоро)", inline=False)
    embed.add_field(name=f"  [TECH] => restart", value=f"Перезапустить бота с новым кодом (скоро)", inline=False)
    embed.add_field(name=f"  [TECH] => bd_check", value=f"Вся информация о и в базе данных бота (скоро)", inline=False)
    embed.add_field(name=f"  [TECH] => git_upd", value=f"Загрузить обновление бота с GitHub репозитория при его наличии (скоро)", inline=False)
    embed.set_footer(text=f"\n Версия бота - {version}")
    await ctx.send(embed=embed)

    #Слэш команда для игры в "Название игры"

@bot.slash_command(name='walk', description='Попробовать прогуляться и найти бонусы!')
async def walk(ctx):
    global dop_data
    embed = Embed(title=f' :evergreen_tree: **Прогулка** :deciduous_tree:', description=f'', color=disnake.Color.blue())
    user_id = ctx.user.id
    user_name = ctx.user.name
    lives = db.db_work.get("lives", user_id, user_name)
    if lives > 20:
        lives -= 20
        rand = randint(1, 260)
        if rand <= 10:
            new_data = [user_id, 1.25]
            db.db_work.upd("exp_buff", 1.25, user_id)
            embed.add_field(name=f"Во время прогулки Вы нашли под деревом забытую скамейку. Теперь героически справлюсь с собственной ленью!", value="Опыт за сообщения повышен на 25%!", inline=False)
        elif rand > 10 and rand <= 20:
            db.db_work.upd("timely", 1.25, user_id)
            embed.add_field(name=f"Хоть Вы и решили просто прогуляться, но в итоге нашли своё потерянное улучшение. Благодать, времени ожидать дожаривания шашлыка не придется!", value="Следующая награда будет увеличена на 25%!", inline=False)
        elif rand > 20 and rand <= 35:
            db.db_work.upd("exp_buff", 0.75, user_id)
            embed.add_field(name=f"Прогуливаясь у водопада, Вы обнаружили пропавшие очки. Может быть, это знак, что следует смотреть на мир с новой перспективы?", value="Получаемый вами опыт снижен на 25%!", inline=False)
        elif rand > 35 and rand <= 50:
            db.db_work.upd("timely", 0.75, user_id)
            embed.add_field(name=f"Во время прогулки Вы нашел потерянную шляпу, в которой оказалось обилие бумажек с записками 'Не забудь купить молоко'. Что ж, переключаясь с шляпника на торговца, Вы отправились в ближайший магазин", value="Следующая получаемая награда снижена на 25%!", inline=False)
        elif rand > 50 and rand <= 55:
            _ = randint(1,2)
            lives += 40
            if _ == 1:
                embed.add_field(name=f"Во время прогулки по парку Вы случайно столкнулись с бегающим енотом и нашли его потерянный предмет - похоже, это что-то необычное!", value="Вы восстановили себе 40 здоровья!", inline=False)
            else:
                embed.add_field(name=f"Во время прогулки Вы случайно наткнулись на потерянный пакетик чая, который, к Вашему удивлению, оказался необычным. После его заваривания Вы получили силы!", value="Вы восстановили себе 40 здоровья!", inline=False)
        elif rand > 55 and rand <= 80:
            lives = 0
            embed.add_field(name=f"Однажды, когда Вы шли через поле, наткнулись на валяющийся пирог. Кажется, было большой ощибкой подбирать его...", value="Ваше здоровье снизилось до 0!", inline=False)
        elif rand > 80 and rand <= 115:
            _ = randint(1,2)
            balance_up(user_id, 100, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы увидели, как собака выкапывала что-то на земле. Оказалось, это был сверхсекретный клад с печеньками", value=f"Вы нашли 100 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Однажды, гуляя в парке, Вы случайно наткнулся на пару кроликов, которые таскали за собой затерянную сокровищницу и вам удалось забрать её!", value=f"Вы нашли 100 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 115 and rand <= 130:
            _ = randint(1,2)
            balance_up(user_id, 200, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы увидели, как собака выкапывала что-то на земле. Оказалось, это был сверхсекретный клад с печеньками", value=f"Вы нашли 200 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Однажды, гуляя в парке, Вы случайно наткнулся на пару кроликов, которые таскали за собой затерянную сокровищницу и вам удалось забрать её!", value=f"Вы нашли 200 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 130 and rand <= 135:
            _ = randint(1,2)
            balance_up(user_id, 300, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы увидели, как собака выкапывала что-то на земле. Оказалось, это был сверхсекретный клад с печеньками", value=f"Вы нашли 300 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Однажды, гуляя в парке, Вы случайно наткнулся на пару кроликов, которые таскали за собой затерянную сокровищницу и вам удалось забрать её!", value=f"Вы нашли 300 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 135 and rand <= 175:
            _ = randint(1,2)
            balance_up(user_id, -150, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы встретили кошку, которая ухитрилась найти затерянный пакет где-то в Ваших карманах. Но после Вы замечаете, что стопка денег была спрятана в пакете...", value=f"Вы потеряли 150 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Бродя по лесу, Вы наткнулись на заблудшую коллекцию губной помады. К сожалению, Вы не смогли устоять перед ними...", value=f"Вы потратили 150 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 175 and rand <= 180:
            _ = randint(1,2)
            balance_up(user_id, -300, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы встретили кошку, которая ухитрилась найти затерянный пакет где-то в Ваших карманах. Но после Вы замечаете, что стопка денег была спрятана в пакете...", value=f"Вы потеряли 300 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Бродя по лесу, Вы наткнулись на заблудшую коллекцию губной помады. К сожалению, Вы не смогли устоять перед ними...", value=f"Вы потратили 300 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 180 and rand <= 195:
            _ = randint(1,2)
            balance_up(user_id, -200, user_name)
            if _ == 1:
                embed.add_field(name=f"Во время прогулки Вы встретили кошку, которая ухитрилась найти затерянный пакет где-то в Ваших карманах. Но после Вы замечаете, что стопка денег была спрятана в пакете...", value=f"Вы потеряли 200 {emoji_perl} Блёбопёрлов!", inline=False)
            else:
                embed.add_field(name=f"Бродя по лесу, Вы наткнулись на заблудшую коллекцию губной помады. К сожалению, Вы не смогли устоять перед ними...", value=f"Вы потратили 200 {emoji_perl} Блёбопёрлов!", inline=False)
        elif rand > 195 and rand <= 200:
            db.db_work.upd("kurs", 0.9, user_id)
            embed.add_field(name=f"Прогуливаясь вдоль озера, Вы неожиданно услышали жуткий крик. Оказалось, это утка нашла потерянные деньги  и устроила настоящий шоу мод!", value=f"Курс обмена для вас поднят до 0.9 {emoji_perl} Блёбопёрлов", inline=False)
        elif rand > 200 and rand <= 210:
            new_data = [user_id, 0.5]
            db.db_work.upd("kurs", 0.5, user_id)
            embed.add_field(name=f"Прогуливаясь вдоль озера, Вы неожиданно услышали жуткий крик. Оказалось, это утка нашла потерянные деньги  и устроила настоящий шоу мод!", value=f"Курс обмена для вас упал до 0.5 {emoji_perl} Блёбопёрлов", inline=False)
        elif rand > 210 and rand <= 260:
            _ = randint(1,2)
            if _ == 1:
                embed.add_field(name=f"Пока Вы шли в парке, наставив ногу на кучу листьев, Вы обнаружили свою бесценную ручку, которую потеряли год назад", value="Something wrong...", inline=False)
            else:
                embed.add_field(name=f"Заглянув под куст, Вы обнаружил улыбающийся камень. Это была настолько позитивная находка, что Вы даже почувствовали в нем душу философа!", value="Что-то не так...", inline=False)
        else:
            pass
        embed.set_footer(text=f" Играет => {user_name}  |  Здоровье => {lives}")
        await ctx.send(embed=embed)
    else:
        embed = Embed(title=f' :evergreen_tree: **Прогулка** :deciduous_tree:', description=f' Увы, но ваши жизни окончены... ', color=disnake.Color.red())
        embed.set_footer(text=f" Играет => {user_name}  |  Здоровье => {lives}")
        await ctx.send(embed=embed)
    db.db_work.upd("lives", lives, user_id)


@bot.slash_command(name='ping', description='Узнать пинг бота')
async def ping(ctx):
    await ctx.send(f' (▽◕ ᴥ ◕▽) Мой ответ занял: ** {round(bot.latency*1000)} мс**')

    #Команда скрытая для отправки сообщения с 6 аргументами

@bot.command()
async def echo(ctx, a, b, c, d, e, f):
    user_id = ctx.user.id
    if user_id == 761668841642000384:
        await ctx.reply(f"{a} {b} {c} {d} {e} {f}")
    else:
        await ctx.reply(f'  => Напишите, пожалуйста, /cmds')
@bot.command()
async def sencured(ctx):
    await ctx.reply(f"Жедоби")
    
#Запуск бота

bot.run(token)
