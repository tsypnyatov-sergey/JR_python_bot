from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import keyboard_main_menu
import config
from utils import FileManager
from utils.enum_path import PATH
main_router = Router()


@main_router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        text= FileManager.read_txt(PATH.MESSAGES,"main"),
        reply_markup=keyboard_main_menu(),
    )

@main_router.message(Command('random'))
async def start_command(message):
    print(message.from_user.id)

@main_router.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f"Пользователь {message.from_user.full_name} написал: \n {message.text}"
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=msg_text,
    )
