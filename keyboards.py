from aiogram.utils.keyboard import ReplyKeyboardBuilder

def keyboard_main_menu():
    keyboard = ReplyKeyboardBuilder()
    buttons = [
        "/random",
        "/gpt",
        "/talk",
        "/quiz",
    ]
    for button in buttons:
        keyboard.button(
            text=button,
        )
    return keyboard.as_markup(resize_keyboard=True)