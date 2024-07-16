import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from tk import token
from database import *
bot=telebot.TeleBot(token)
from text import txt

text = txt()
db = database()
key = []
log = {}
edit_item={}

@bot.message_handler(commands=['start', "help"])
def start_message(message):
    db.create_db()
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b1 = KeyboardButton(text="опр")
    b2 = KeyboardButton(text="изм")
    kb.add(b1, b2)
    print(log)
    bot.send_message(chat_id=message.chat.id, text="<b>"+text.start+"</b>", reply_markup=kb, parse_mode="HTML")


@bot.message_handler(content_types="text")
def text_message_handler(message):
    try:
        if log[message.chat.id]=={}:pass
    except:log[message.chat.id]={
        "audio":None,
        "year":None,
        "job":None,
        "1":None, 
        "2":None, 
        "3":None, 
        "4":None, 
        "5":None, 
        "6":None, 
        "7":None,
    }
    
    if message.text in ["опр", "Опр"]:
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Да", callback_data="1-yes")
        b2 = InlineKeyboardButton(text="Нет", callback_data="1-no")
        b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
        kb.add(b1).add(b2).add(b3)
        bot.send_message(chat_id=message.chat.id, text = "<b>"+text.opr1+"</b>", reply_markup=kb, parse_mode="HTML")
    if message.text in ["изм", "Изм"]:
        edit_1(message)


    key_break=False
    print(key)
    for item in key:
        if message.chat.id==item["id"]:
            log[message.chat.id][str(item["number"])]=message.text
            key.remove(item)
            key_break=True
            print("break")
            break
    if key_break:
        if item["number"]==3:
            print("go_to_4_2_from_message_text")
            opr4_2(message)
        elif item["number"]==4:
            print("go_to_5_from_message_text")
            log[message.chat.id]["4"]=message.text
            opr5_message(message)
        elif item["number"]==5:
            log[message.chat.id]["5"]=message.text
            opr7_message(message)
        elif item["number"]==6:
            log[message.chat.id]["6"]=message.text
            opr7_message(message)
        elif item["number"]==7:
            log[message.chat.id]["7"]=message.text
            end_1(message)


@bot.callback_query_handler(func=lambda  callback: callback.data)
def check_callback_data(callback):
    if callback.data=="end-opr":
        save_log(callback)
    
    if callback.data[0]=="1":
        opr2(callback)
    
    if callback.data[0]=="2":
        opr3(callback)
    
    if callback.data[0]=="3":
        opr4_1(callback)

    if  callback.data=="4-scip":
        key.remove({"id":callback.message.chat.id, "number":4})
        opr5_callback(callback)

    if callback.data[0]=="5":
        if callback.data=="5-yes":
            log[callback.message.chat.id]["5"]=callback.data[2:]
            opr6(callback)
        if callback.data=="5-no":
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton(text="Пропустить", callback_data="5-scip")).add(InlineKeyboardButton(text="Закончить", callback_data="end-opr"))
            key.append({"id":callback.message.chat.id, "number":5})
            bot.send_message(chat_id=callback.message.chat.id, text="<b>Причина?</b>",reply_markup=kb, parse_mode="HTML")

    if callback.data == "5-scip":
        key.remove({"id":callback.message.chat.id, "number":5})
        opr7_message(callback.message)

    if callback.data=="6-scip":
        key.remove({"id":callback.message.chat.id, "number":6})
        opr7_message(callback.message)
    
    if callback.data=="7-scip":
        key.remove({"id":callback.message.chat.id, "number":7})
        end_1(callback.message)
    
    if "edit_" in callback.data:
        edit_3(callback)

def save_log(callback):
    data=log[callback.message.chat.id]
    db.add_data(data=data)
    log[callback.message.chat.id]={
        "audio":None,
        "year":None,
        "job":None,
        "1":None, 
        "2":None, 
        "3":None, 
        "4":None, 
        "5":None, 
        "6":None, 
        "7":None,
    }

def opr2(callback):
    log[callback.message.chat.id]["1"]=callback.data[2:]
    kb = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="Да", callback_data="2-yes")
    b2 = InlineKeyboardButton(text="Нет", callback_data="2-no")
    b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
    kb.add(b1).add(b2).add(b3)
    bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr2+"</b>", reply_markup=kb, parse_mode="HTML")


def opr3(callback):
    log[callback.message.chat.id]["2"]=callback.data[2:]

    # {Если ответ на 2-й вопрос нет}
    if callback.data[2:]=="no":
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Да", callback_data="3-yes")
        b2 = InlineKeyboardButton(text="Нет", callback_data="3-no")
        b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
        kb.add(b1).add(b2).add(b3)
        bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr3_1+"</b>", reply_markup=kb, parse_mode="HTML")
    else:
        kb = InlineKeyboardMarkup()
        b2 = InlineKeyboardButton(text="Пропустить вопрос", callback_data="3-scip")
        b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
        kb.add(b2).add(b3)
        bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr3_2+"</b>", reply_markup=kb, parse_mode="HTML")
        key.append({"id":callback.message.chat.id, "number":3})

#Если использовался вопрос 3.1
def opr4_1(callback):
    if callback.data!="3-scip":
        log[callback.message.chat.id]["3"]=callback.data[2:]
    
    if  log[callback.message.chat.id]["2"]=="no" and \
    log[callback.message.chat.id]["3"]=="yes":
        kb = InlineKeyboardMarkup()
        b2 = InlineKeyboardButton(text="Пропустить вопрос", callback_data="4-scip")
        b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
        kb.add(b2).add(b3)
        bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr4+"</b>", reply_markup=kb, parse_mode="HTML")
        key.append({"id":callback.message.chat.id, "number":4})
    else:
        opr5_callback(callback)

#Если использовался вопрос 3.2
def opr4_2(message):
    log[message.chat.id]["3"]=message.text
    if  log[message.chat.id]["1"]=="no" and \
    log[message.chat.id]["2"]=="yes":
        kb = InlineKeyboardMarkup()
        b2 = InlineKeyboardButton(text="Пропустить вопрос", callback_data="4-scip")
        b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
        kb.add(b2).add(b3)
        bot.send_message(chat_id=message.chat.id, text="<b>"+text.opr4+"</b>", reply_markup=kb, parse_mode="HTML")
        key.append({"id":message.chat.id, "number":4})
    else:
        opr5_message(message)

def opr5_callback(callback):
    try: key.remove({"id":callback.message.chat.id, "number":3})#очистка ключей ожидания
    except: pass

    if callback.data[0]=="3":
        if callback.data!="3-scip":
            log[callback.message.chat.id]["3"]=callback.data[2:]
    print(log)
    kb = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="Да", callback_data="5-yes")
    b2 = InlineKeyboardButton(text="Нет, почему? ↓",callback_data="5-no")
    b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
    kb.add(b1).add(b2).add(b3)
    bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr5+"</b>",reply_markup=kb, parse_mode="HTML")

def opr5_message(message):
    print(log)
    kb = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="Да", callback_data="5-yes")
    b2 = InlineKeyboardButton(text="Нет, почему? ↓",callback_data="5-no")
    b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
    kb.add(b1).add(b2).add(b3)
    bot.send_message(chat_id=message.chat.id, text="<b>"+text.opr5+"</b>",reply_markup=kb, parse_mode="HTML")

def opr6(callback):
    kb = InlineKeyboardMarkup()
    b2 = InlineKeyboardButton(text="Пропустить вопрос", callback_data="6-scip")
    b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
    kb.add(b2).add(b3)
    key.append({"id": callback.message.chat.id, "number": 6})
    bot.send_message(chat_id=callback.message.chat.id, text="<b>"+text.opr6+"</b>", reply_markup=kb, parse_mode="HTML")

def opr7_message(message):
    print(f"7: {log}")
    kb = InlineKeyboardMarkup()
    b2 = InlineKeyboardButton(text="Пропустить вопрос", callback_data="7-scip")
    b3 = InlineKeyboardButton(text="Закончить", callback_data="end-opr")
    kb.add(b2).add(b3)
    key.append({"id": message.chat.id, "number": 7})
    bot.send_message(chat_id=message.chat.id, text="<b>"+text.opr7+"</b>", reply_markup=kb, parse_mode="HTML")

def end_1(message):
    db.add_data(data=log[message.chat.id])
    l = db.len_db()
    kb = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text="Продолжить", callback_data="to_end_2")
    kb.add(b)
    bot.send_message(chat_id=message.chat.id, text=f"<b>Опрос окончен! \nid записи: {l}\nНе заполненные поля: {[x for x in log[message.chat.id] if log[message.chat.id][x]==None]}</b>", reply_markup=kb, parse_mode="HTML")

def edit_1(message):
    edit_item[message.chat.id]={}
    msg = bot.send_message(chat_id=message.chat.id, text="Какой id изменить? 0-отмена")
    bot.register_next_step_handler(msg, edit_2)


def edit_2(message):
    edit_item[message.chat.id]["id"]=message.text
    if int(message.text) > db.len_db():
        edit_1(message)
    elif message.text=="0":
        pass
    else:
        kb = InlineKeyboardMarkup()
        for item in log[message.chat.id]:
            b = InlineKeyboardButton(text=f"edit_{item}", callback_data=f"edit_{item}")
            kb.add(b)
        bot.send_message(chat_id=message.chat.id, text="<b>Выбери пункт, который хочешь изменить</b>", reply_markup=kb, parse_mode="HTML")

def edit_3(callback):
    edit_item[callback.message.chat.id]["item"] = callback.data.replace("edit_", "")
    msg = bot.send_message(chat_id=callback.message.chat.id, text="<b>Введи новый текст(для кнопок да/нет - yes/no соответственно, delete-удалить значение)</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, edit_4)

def edit_4(message):
    if edit_item[message.chat.id]["item"]=="audio":
        if message.text=="delete":
            db.edit(id = edit_item[message.chat.id]["id"],data={edit_item[message.chat.id]["item"]:None})
        else:
            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'./audio/{edit_item[message.chat.id]["id"]}.m4a'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.edit(id = edit_item[message.chat.id]["id"],data={"audio":src})
    else:
        if message.text=="delete":
            message.text=None
        db.edit(id = edit_item[message.chat.id]["id"],data={edit_item[message.chat.id]["item"]:message.text})


    bot.send_message(chat_id=message.chat.id, text="<b>Изменено!</b>", parse_mode="HTML")
bot.infinity_polling()

