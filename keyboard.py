from aiogram import types

agr_button = [
    [types.KeyboardButton(text='Агрегация')]
]

button = types.ReplyKeyboardMarkup(keyboard=agr_button, resize_keyboard=True)