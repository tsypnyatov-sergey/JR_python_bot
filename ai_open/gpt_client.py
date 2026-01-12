import httpx
import openai
from aiogram import Bot

import config
from ai_open.enums import GPTModel #гпт пишет что такой импорт лучше. До этого был from .enums
from ai_open.messages import GPTMessage #гпт пишет что такой импорт лучше. До этого был from .messages



class GPTService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance =super().__new__(cls)
        return cls._instance

    def __init__(self, model: GPTModel = GPTModel.GPT_3_TURBO):
        self._gpt_token = config.OPENAI_API_KEY
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
        )
        return gpt_client

    async def request(self,message_list: GPTMessage, bot:Bot) ->str:
        try:
            response = await self._client.chat.completions.create(
                messages = message_list.message_list,
                model = self._model,
            )
            return response.choices[0].message.content
        except Exception as e:
            await bot.send_message(
                chat_id = config.ADMIN_ID,
                text = str(e),
            )
            return "Ошибка при обращении к GPT.Попробуйте позже"

