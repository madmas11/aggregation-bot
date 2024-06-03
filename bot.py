import asyncio
import json
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from aggregate import aggregate_salaries
from keyboard import button


load_dotenv()

BOT_TOKEN = os.getenv('TOKEN_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

error_messages = {'type': 'Неверный формат типа агрегации. Должно быть hour, day, month.',
                  'request': 'Неправильный запрос. Нужно в формате JSON.'}
example_message = '''
Пример данных: {"dt_from": "2022-02-01T00:00:00",
                "dt_upto": "2022-02-02T00:00:00",
                "group_type": "hour"}'''

KEYS = ['dt_from', 'dt_upto', 'group_type']
GROUPS = ['hour', 'day', 'month']


@dp.message(CommandStart())
async def hello(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}, это бот для агрегации данных '
                         'о зарплатах сотрудников компании по временным промежуткам. '
                         'Нажми на кнопку для дальнейшего действия.',
                         reply_markup=button)


@dp.message(F.text == 'Агрегация')
async def aggregation(message: types.Message):
    await message.answer('Отправь данные в формате JSON.')
    await message.answer(example_message)


async def get_data(message: types.Message):
    try:
        dict_message = json.loads(message.text)
        return dict_message
    except json.JSONDecodeError:
        await message.answer(error_messages['request'])
        await message.answer(example_message)


@dp.message(F.text)
async def agr(message: types.Message):
    if not message.text.startswith('{'):
        await message.answer(error_messages['request'])
    else:
        dict_message = await get_data(message)
        for key in dict_message:
            if key not in KEYS:
                await message.answer(f'Такого ключа "{key}" нет.')
                await message.answer(f'Вот пример {example_message}')
                return

        dt_from = dict_message['dt_from']
        dt_upto = dict_message['dt_upto']
        group_type = dict_message['group_type']
        if group_type not in GROUPS:
            await message.answer(error_messages['type'])
        try:
            result = aggregate_salaries(dt_from, dt_upto, group_type)
            return await message.answer(str(result))
        except ValueError as e:
            await message.answer(str(e))


async def main():
    while True:
        await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
