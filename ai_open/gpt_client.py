import httpx
import openai
from aiogram import Bot

import config
from .enums import GPTModel
from .gpt_message import GPTMessage


class GPTService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance is None:
            cls._instance =super().__new__(cls)
        return cls._instance

    def __init__(self, model: GPTModel = GPTModel.GPT_4_TURBO):
        self._gpt_token = config.OPEN_API_KEY
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value

    def _create_client(self):
        gpt_client = openai.AsyncOpenAi(
            api_key=self._gpt_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
        )
        return gpt_client

    async def request(self,message_list: GPTMessgae, bot:Bot) ->str:
        try:
            response = await self._client.chat.completions.create(
                messgae = message_list.message_list,
                model = self._model,
            )
            return response.choice[0].message.content
        except Exception as e:

