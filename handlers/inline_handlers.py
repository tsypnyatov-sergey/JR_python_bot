from aiogram import Router, Bot, F
from aiogram.enums.chat_action import ChatAction
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

from .fsm import GPTRequest, CelebrityTalk, Quiz
from aiogram.fsm.context import FSMContext
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from keyboards import ikb_main_menu, ikb_random, ikb_cancel_gpt, ikb_talk_menu, ikb_talk_back, ikb_quiz_menu, ikb_quiz_back
from keyboards.callback_data import CallbackMenu,CallbackTalk, CallbackQuiz
from utils import FileManager
from utils.enum_path import PATH

from ai_open.enums import GPTRole

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


@inline_router.callback_query(CallbackMenu.filter(F.button == "talk"))
async def talk_menu(callback: CallbackQuery, callback_data: CallbackMenu,state: FSMContext, bot: Bot):
    await state.clear()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(PATH.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_talk_menu()
    )

@inline_router.callback_query(CallbackTalk.filter(F.button == "talk"))
async def talk_with_celebrity(callback: CallbackQuery, callback_data: CallbackMenu,state: FSMContext, bot: Bot):
    await state.set_state(CelebrityTalk.dialog)
    message_list = GPTMessage(callback_data.celebrity)
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages = message_list, celebrity = callback_data.celebrity )

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.celebrity)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_talk_back(),
    )


@inline_router.callback_query(CallbackMenu.filter(F.button == "quiz"))
async def quiz_menu(callback: CallbackQuery, callback_data: CallbackMenu,state: FSMContext, bot: Bot):
    await state.set_state(Quiz.game)
    messages = await state.get_value("messages")
    if not messages:
        await state.update_data(score=0, messages = None, message_id= callback.message.message_id )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(PATH.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_quiz_menu(),
    )

@inline_router.callback_query(CallbackQuiz.filter(F.button == "quiz"))
async def select_subject(callback: CallbackQuery, callback_data: CallbackQuiz,state: FSMContext, bot: Bot):
    message_list = await state.get_value("messages")
    if not message_list:
        message_list = GPTMessage("quiz")
    message_list.update(GPTRole.USER, callback_data.subject)
    response = await chat_gpt.request(message_list, bot)
    await state.update_data(messages = message_list)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(PATH.IMAGES.value.format(file=callback_data.button)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_quiz_back(),
    )