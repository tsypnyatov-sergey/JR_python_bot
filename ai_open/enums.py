from enum import Enum

class GPTRole(Enum):
    USER = "user"
    CHAT = "assistant"
    SYSTEM = "system"

class GPTModel(Enum):
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_4_MINI = "gpt-4.1-mini"
    WHISPER ="whisper-1"  #обработка голосовых сообщений
    GPT_IMAGE = "dall-e-3" #обработка изображений