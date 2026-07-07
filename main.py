import telebot
import json
import os
from flask import Flask
import threading

TOKEN = "8814574714:AAH4ywvUNzmzJSiilct9EnVADKgLsBuSdFU"
ADMIN_ID = 8765424371
bot = telebot.TeleBot(TOKEN)
FILE = "data.json"

app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

data = load()

def get_id(m):
    return str(m.from_user.id)

@bot.message_handler(commands=['start'])
def start(m):
    uid = get_id(m)
    if uid not in data:
        data[uid] = {"points": 0, "phone": ""}
        save(data)
    bot.reply_to(m, "اهلا بيك في البوت \nرصيدك: " + str(data[uid]["points"]))

@bot.message_handler(commands=['points'])
def points(m):
    uid = get_id(m)
    if uid not in data:
        data[uid] = {"points": 0, "phone": ""}
        save(data)
    bot.reply_to(m, "رصيدك: " + str(data[uid]["points"]))

@bot.message_handler(commands=['charge'])
def charge(m):
    if m.from_user.id!= ADMIN_ID:
        bot.reply_to(m, "انت مش الادمن")
        return
    try:
        msg = m.text.split()
        uid = msg[1]
        amount = int(msg[2])
        if uid in data:
            data[uid]["points"] += amount
            save(data)
            bot.reply_to(m, f"تم شحن {amount} نقاط للايدي {uid}")
            bot.send_message(int(uid), f"تم شحن رصيدك بـ {amount} نقاط")
        else:
            bot.reply_to(m, "الايدي ده مش موجود")
    except:
        bot.reply_to(m, "الاستخدام: /charge ID المبلغ")

@bot.message_handler(commands=['users'])
def users(m):
    if m.from_user.id!= ADMIN_ID:
        return
    msg = "المستخدمين:\n"
    for uid, info in data.items():
        msg += f"ID: {uid} | رصيد: {info['points']}\n"
    bot.reply_to(m, msg)

threading.Thread(target=run_flask).start()
bot.polling(none_stop=True)
