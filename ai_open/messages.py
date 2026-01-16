from utils import FileManager
from .enums import GPTRole
from utils.enum_path import PATH

class GPTMessage:

    def __init__(self, prompt:str, message_list:list[dict[str,str]] | None=None):
        self._prompt_path = prompt
        self.message_list = message_list if message_list else self._init_message()
# вот здесь нужно как то прописать чтобы он не запомнила всю историю переписки, а помнил 5-6 сообщений. Удалял с первого и добавлял в конец 
    def _init_message(self) -> list[dict[str,str]]:
        message = {
            "role": GPTRole.SYSTEM.value,
            "content": self._load_prompt(),
        }
        return [message]

    def _load_prompt(self) -> str:
        prompt = FileManager.read_txt(PATH.PROMPTS,self._prompt_path)
        return prompt

    def update(self, role: GPTRole, message: str):
        message = {
            "role": role.value,
            "content": message,
        }
        self.message_list.append(message)