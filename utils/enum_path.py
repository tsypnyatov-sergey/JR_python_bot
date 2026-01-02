import os
from enum import Enum

class PATH(Enum):
    PROMPTS = os.path.join("resources", "prompts")
    MESSAGES = os.path.join("resources", "messages")