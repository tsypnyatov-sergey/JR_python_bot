from aiogram.utils.keyboard import  InlineKeyboardBuilder
from collections import namedtuple
from .callback_data import CallbackMenu

Button = namedtuple("Button", ["text","callback"])

def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button("Рандомный факт", "random"),
        Button("Спросить GPT", "gpt"),
        Button("Разговор со звездой", "talk"),
        Button("КВИЗ!", "quiz"),
    ]


    for button in buttons:
        keyboard.button(
            text=button.text,
            callback_data = CallbackMenu(button = button.callback)

        )
    keyboard.adjust(2,2)
    return keyboard.as_markup()


def ikb_random():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        "Хочу еще факт!",
        "Закончить",

    ]

    for button in buttons:
        keyboard.button(
            text=button,
            callback_data="1",
        )
    return keyboard.as_markup()