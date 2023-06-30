from googletrans import Translator

import aiogram
import config as cfg
import sqlite3
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

HISTORYMSG = "Выберите пользователя, чью историю хотите посмотреть"
name = None
transl = Translator()

con = sqlite3.connect('db.sqlite')
storage = MemoryStorage()
bot = aiogram.Bot(token=cfg.TOKEN)

dp = aiogram.Dispatcher(bot, storage=storage)
print('started')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):

    cur = con.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS texts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_name INTEGER NOT NULL,
        FOREIGN KEY(user_name) REFERENCES users(name)
    );
    ''')
    global your_name
    your_name = msg.from_user.username
    cur.execute("SELECT * FROM users WHERE users.name = '%s'" % (your_name))
    myresult = cur.fetchall()
    print(myresult)

    if myresult is None or myresult == [] or myresult == ():
        cur.execute("INSERT INTO users(name) VALUES ('%s')" % (your_name))
        con.commit()
        await msg.reply("Привет! Вы зарегестрированы!")
    else:
        await msg.reply("Вы уже были зарегестрированы!")

    cur.execute('SELECT * FROM users')
    print(cur.fetchall())
    cur.close()
    con.close()


@dp.message_handler(commands=['history'])
async def process_history_command(message: types.Message):
    keyb = InlineKeyboardMarkup()

    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute(
        "SELECT users.name FROM users"
        )
    arr = []
    for result in cur:
        arr.append(result[0])

    for i in arr:
        key = InlineKeyboardButton(i, callback_data=i)
        keyb.add(key)
    await message.reply(HISTORYMSG, reply_markup=keyb)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global your_name
    your_name = callback_query.from_user.username
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
        SELECT texts.name
        FROM texts
        WHERE texts.user_name = "%s"
        ''' % (callback_query.data)
        )
    result = cur.fetchall()
    print(callback_query.data)
    print(result)
    arr = []
    for i in result:
        arr.append(i[0])
    await bot.send_message(callback_query.from_user.id, '\n'.join(arr))


@dp.message_handler()
async def echo_message(msg: types.Message):
    word = transl.translate(msg.text, dest='ru').text
    con_text = msg.text + ' - ' + word
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
    INSERT INTO texts(name, user_name) VALUES ('%s', '%s')
    ''' % (con_text, your_name)
    )
    con.commit()
    cur.execute('SELECT * FROM texts')
    print(cur.fetchall())
    cur.close()
    con.close()

    await bot.send_message(msg.chat.id, word)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
