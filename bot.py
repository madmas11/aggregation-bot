import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from keyboard import button
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def hello(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}, это бот для агрегации данных '
                         'о зарплатах сотрудников компании по временным промежуткам. '
                         'Нажми на кнопку для дальнейшего действия.',
                         reply_markup=button)


async def main():
    while True:
        await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
