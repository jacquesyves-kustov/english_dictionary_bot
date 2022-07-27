from enum import Enum
from bot_engine import Smiles


# enum для генерации текстов уведомлений
class Messages(Enum):
    HELLO = Smiles.VICTORY_HAND.value + " Привет, {}!"
    EMPTY_WORD_LIST = "В изучении английского языка важна регулярность. Самое время выучить новые слова!"
    NOTIFICATION_DEFAULT_TEXT = "Напоминаем тебе о словах, которые ты изучаешь:\n\n\n"
