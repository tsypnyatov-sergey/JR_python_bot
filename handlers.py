from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from aiogram.enums.chat_action import ChatAction

import config
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from keyboards import ikb_main_menu, ikb_random
from utils import FileManager
from utils.enum_path import PATH

main_router = Router()


# хендлер, который обрабатывает все команды и подставляет изображение
@main_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject):
        await message.answer_photo(
        photo=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_txt(PATH.MESSAGES, command.command),
        reply_markup=ikb_main_menu(),
    )


# КОМАНДА РАНДОМ
@main_router.message(Command("random"))
async def random_handler(message: Message, command: CommandObject, bot: Bot):
    sent_message = await message.answer_photo(                                      #правка sent_message от гпт
        photo=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_txt(PATH.MESSAGES, command.command),
    )

    await bot.send_chat_action(
        chat_id = message.chat.id,
        action = ChatAction.TYPING,
    )

    response = await chat_gpt.request(GPTMessage('random'), bot)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=command.command)),
            caption=response,

        ),
        chat_id=sent_message.chat.id, #используем chat.id, вместо from_user_id
        message_id=sent_message.message_id, #убрали +1
        reply_markup = ikb_random(),

    )


# сообщает админу какой пользователь что написал
@main_router.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f"Пользователь {message.from_user.full_name} написал: \n {message.text}"
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=msg_text,
    )
