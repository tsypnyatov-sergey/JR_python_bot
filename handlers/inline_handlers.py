from aiogram import Router, Bot, F
from aiogram.enums.chat_action import ChatAction
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

from .fsm import GPTRequest
from aiogram.fsm.context import FSMContext
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from keyboards import ikb_main_menu, ikb_random, ikb_cancel_gpt
from keyboards.callback_data import CallbackMenu
from utils import FileManager
from utils.enum_path import PATH

inline_router = Router()

@inline_router.callback_query(CallbackMenu.filter(F.button == "start"))
async def main_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(PATH.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,  # используем chat.id, вместо from_user_id
        message_id=callback.message.message_id,
        reply_markup = ikb_main_menu()
    )

# КОМАНДА РАНДОМ
@inline_router.callback_query(CallbackMenu.filter(F.button == "random"))
async def random_handler(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot):
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(PATH.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,  # используем chat.id, вместо from_user_id
        message_id=callback.message.message_id,
    )

    await bot.send_chat_action(
        chat_id = callback.from_user.id,
        action = ChatAction.TYPING,
    )

    response = await chat_gpt.request(GPTMessage('random'), bot)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=response,

        ),
        chat_id=callback.from_user.id, #используем chat.id, вместо from_user_id
        message_id=callback.message.message_id,
        reply_markup = ikb_random(),

    )

@inline_router.callback_query(CallbackMenu.filter(F.button == "gpt"))
async def gpt_menu(callback: CallbackQuery, callback_data: CallbackMenu,state: FSMContext, bot: Bot):
    await state.set_state(GPTRequest.wait_for_request)
    await state.update_data(
        message_id=callback.message.message_id,
    )

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(PATH.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_cancel_gpt()
    )


