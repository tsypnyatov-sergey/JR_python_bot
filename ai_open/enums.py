from enum import Enum

class GPTRole(Enum):
    USER = "user"
    CHAT = "assistance"
    SYSTEM = "system"

class GPTModel(Enum):
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_4_TURBO = "gpt-4"
    WHISPER ="whisper-1"  #обработка голосовых сообщений
    GPT_IMAGE = "dall-e-3" #обработка изображений