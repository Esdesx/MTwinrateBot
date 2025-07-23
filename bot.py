
import logging
from aiogram import Bot, Dispatcher, executor, types
import os

API_TOKEN = os.getenv('API_TOKEN')  # Получаем токен из переменной окружения

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Введи общее количество боев:")
    user_data[message.from_user.id] = {}

@dp.message_handler(lambda message: message.text.isdigit())
async def collect_numbers(message: types.Message):
    uid = message.from_user.id
    state = user_data.get(uid, {})

    if 'battles' not in state:
        state['battles'] = int(message.text)
        await message.reply("Сколько побед?")
    elif 'wins' not in state:
        state['wins'] = int(message.text)
        await message.reply("Какой процент побед ты хочешь (например, 56)?")
    elif 'target' not in state:
        state['target'] = float(message.text) / 100
        await message.reply("С каким процентом ты планируешь побеждать (например, 66.67 или 75)?")
    elif 'future_rate' not in state:
        state['future_rate'] = float(message.text) / 100

        N = state['battles']
        W = state['wins']
        target = state['target']
        r = state['future_rate']

        if r <= target:
            await message.reply("Ты не сможешь достичь цели, если твой винрейт ниже цели!")
            return

        x = (target * N - W) / (r - target)
        x = int(x) + 1

        await message.reply(f"Тебе нужно сыграть примерно {x} боев, чтобы достичь {int(target*100)}% при винрейте {int(r*100)}%.")
        user_data.pop(uid, None)
    else:
        await message.reply("Начни заново /start")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
