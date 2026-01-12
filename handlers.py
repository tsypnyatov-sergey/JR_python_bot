from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

import config
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from keyboards import keyboard_main_menu
from utils import FileManager
from utils.enum_path import PATH

main_router = Router()


# хендлер, который обрабатывает все команды и подставляет изображение
@main_router.message(Command('start', "quiz", "talk", "gpt", ))
async def command_command(message: Message, command: CommandObject):
    keyboard = None
    if command.command == "start":
        keyboard = keyboard_main_menu()
    await message.answer_photo(
        photo=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_txt(PATH.MESSAGES, command.command),
        reply_markup=keyboard,
    )


# КОМАНДА РАНДОМ
@main_router.message(Command("random"))
async def random_handler(message: Message, command: CommandObject, bot: Bot):
    await message.answer_photo(
        photo=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_txt(PATH.MESSAGES, command.command),
    )

    response = await chat_gpt.request(GPTMessage('random'), bot)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
            caption=response,

        ),
        chat_id=message.from_user.id,
        message_id=message.message_id+1,

    )


# сообщает админу какой пользователь что написал
@main_router.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f"Пользователь {message.from_user.full_name} написал: \n {message.text}"
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=msg_text,
    )
