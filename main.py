from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import config

bot = Bot(token = config.BOT_TOKEN)

dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer(f"{message.from_user.full_name}, приветствую тебя! Как твое здоровье?")

@dp.message()
async def all_messages(message: Message):
    await message.answer(
        text= "Я рад, что у тебя все в порядке!"
    )

async def start_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())