# import deepl
# translator = deepl.Translator(auth_key) 
# result = translator.translate_text("Hello world!", target_lang='RU') 
# translated_text = result.text
"""
This is a echo bot.
It echoes any incoming text messages.
"""

from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

transl = Translator()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)