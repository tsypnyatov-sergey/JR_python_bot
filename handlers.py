from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from keyboards import keyboard_main_menu
import config
from utils import FileManager
from utils.enum_path import PATH
main_router = Router()

# хендлер, который обрабатывает все команды и подставляет изображение
@main_router.message(Command('start', "random","quiz","talk","gpt",))
async def command_command(message: Message, command: CommandObject):
    keyboard = None
    if command.command == "start":
        keyboard = keyboard_main_menu()
    await message.answer_photo(
        photo = FSInputFile(PATH.IMAGES.value.format(file = command.command)),
        caption= FileManager.read_txt(PATH.MESSAGES,command.command),
        reply_markup=keyboard,
    )


#сообщает админу какой пользователь что написал
@main_router.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f"Пользователь {message.from_user.full_name} написал: \n {message.text}"
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=msg_text,
    )
