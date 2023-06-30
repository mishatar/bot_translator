import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_keyboard():
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
    return keyb
