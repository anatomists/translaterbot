import config
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types

# задаём уровень логов
logging.basicConfig(level=logging.INFO)

# инициализация бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

def translater(word):
    headers_auth = {'Authorization': 'Basic ' + config.KEY}
    auth = requests.post(config.URL_AUTH, headers=headers_auth)
    if auth.status_code == 200:
        token = auth.text
        while True:
            try:
                word = word
            except KeyboardInterrupt:
                return 'До свидания!'
                exit(0)
            if word:
                headers_translate = {
                    'Authorization': 'Bearer ' + token
                }
                params = {
                    'text': word,
                    'srcLang': 1033,
                    'dstLang': 1049
                }
                r = requests.get(config.URL_TRANSLATE, headers=headers_translate, params=params)
                res = r.json()
                try:
                    return res['Translation']['Translation']

                except:
                    return 'Не найдено варианта для перевода'

    else:
        print('Error')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm TranslaterBot!")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def translate(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    word = message.text
    await message.reply(translater(word))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
