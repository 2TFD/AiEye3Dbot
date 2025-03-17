from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    reply_keyboard_remove, WebAppInfo
from aiogram.utils.keyboard import KeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardBuilder
from fastapi_cli.cli import callback

from cfg import FastServer



adminKB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='настройки', callback_data='settings')
    ]
])

StartKb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='профиль')
    ],
    [
        KeyboardButton(text='покупка токенов')
    ],
    [
        KeyboardButton(text='генерация моделей')
    ]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='стоимость  токенов', callback_data='price1token')
    ],
    [
        InlineKeyboardButton(text='количество токенов для старта', callback_data='startTokens')
    ],
    [
        InlineKeyboardButton(text='стоимость генерации', callback_data='priceGen')
    ]
])

numtokens = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='100', callback_data='100')
    ],
    [
        InlineKeyboardButton(text='500', callback_data='500')
    ],
    [
        InlineKeyboardButton(text='1000', callback_data='1000')
    ]
])





async def CheckModel(name):
    keyboard = InlineKeyboardBuilder()
    url = f'{FastServer}/{name}'
    keyboard.add(InlineKeyboardButton(text='осмотреть', web_app=WebAppInfo(url=url)))
    return keyboard.as_markup()