from googletrans import Translator

import aiogram
import config as cfg
import sqlite3
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
TEXT = "Привет! Введите ваше имя"
name = None
transl = Translator()

con = sqlite3.connect('db.sqlite')
storage = MemoryStorage()
bot = aiogram.Bot(token=cfg.TOKEN)

dp = aiogram.Dispatcher(bot, storage=storage)
print('started')


class AwaitMessages(StatesGroup):
    name = State()
    text = State()


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
        type_id INTEGER NOT NULL,
        FOREIGN KEY(type_id) REFERENCES users(id)
    );
    ''')

    con.commit()
    cur.close()
    con.close()
    await bot.send_message(msg.chat.id, TEXT)
    await AwaitMessages.name.set()


@dp.message_handler(state=AwaitMessages.name)
async def process_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = msg.text.strip()
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO users(name) VALUES ('%s')" % (data["name"]))
    con.commit()
    cur.execute('SELECT * FROM users')
    print(cur.fetchall())
    cur.close()
    con.close()
    await AwaitMessages.text.set()


# @dp.message_handler()
# async def user_name(msg: types.Message):
#     name = msg.text.strip()
#     cur = con.cursor()
#     cur.execute("INSERT INTO users(name) VALUES ('%s')" % (name))
#     con.commit()
#     cur.close()
#     con.close()
#     cur = con.cursor()
#     cur.execute('SELECT * FROM users')
#     await print(cur.fetchall())


@dp.message_handler(state=AwaitMessages.text)
async def echo_message(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = msg.text.strip()
    word = transl.translate(data["text"], dest='ru').text

    await bot.send_message(msg.chat.id, word)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
