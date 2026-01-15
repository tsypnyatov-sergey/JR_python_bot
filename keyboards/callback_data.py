from aiogram.filters.callback_data import CallbackData

class CallbackMenu(CallbackData, prefix = "CM"):
    button: str

class CallbackTalk(CallbackData, prefix = "CT"):
    button: str
    celebrity: str