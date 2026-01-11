from enum import Enum

class GPTRole(Enum):
    USER = "user"
    CHAT = "assistance"
    SYSTEM = "system"

class GPTModel(Enum):
    GPT_3_TURBO = "gpt_3.5-turbo"
    GPT_4_TURBO = "gpt_4-turbo"
    WHISPER ="whisper-1"  #обработка голосовых сообщений
    GPT_IMAGE = "dall-e-3" #обработка изображений