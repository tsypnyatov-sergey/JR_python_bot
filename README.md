# JR Python Bot

Telegram-бот с викториной и интеграцией GPT.

## Стек
- Python 3.11
- aiogram
- FSM
- OpenAI API

## Функциональность
- Диалоговый режим с использованием ChatGPT
- Имитация общения со знаменитостью на основе системного prompt
- Игровая викторина (quiz) с подсчетом очков 
- Управление состояниями пользователя через FSM
- Генерация случайных интересных фактов

## Запуск проекта
1. Клонировать репозиторий:
   git clone https://github.com/tsypnyatov-sergey/JR_python_bot.git

2. Установить зависимости:
   pip install -r requirements.txt

3. Создать файл .env и указать:
   BOT_TOKEN=...
   OPENAI_API_KEY=...

4. Запустить:
   python main.py
