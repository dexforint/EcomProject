from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад")],
        [KeyboardButton(text="/test"), KeyboardButton(text="Вконец")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Введите текст!!!",
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Hello1", url="https://google.com")],
    ]
)


async def inline(cars):
    keyboard = ReplyKeyboardBuilder()
    # keyboard = InlineKeyboardBuilder()

    for car in cars:
        keyboard.add(KeyboardButton(text=car))
        # keyboard.add(InlineKeyboardButton(text="Hello1", url="https://google.com"))

    return keyboard.adjust(2).as_markup()
