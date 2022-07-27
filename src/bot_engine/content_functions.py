from random import choice
from .content_strings import Message, INSPIRATION_PHRASES, RANDOM_WORDS_ECHO


class MessageHandler:
    @staticmethod
    def get_hello_string(name: str) -> str:
        """Возвращает строку для приветствия конкретного юзера"""

        return Message.HELLO.value.format(name)

    @staticmethod
    def get_random_word_string(word: str, word_meanings: dict) -> str:
        """Возвращает строку со случайным словом и его значениями"""

        result = Message.RANDOM_WORD.value.format(word) + "\n\n"

        for meaning in word_meanings[word]:
            result += "\n" + f"_{meaning}_: {word_meanings[word][meaning]}" + "\n"

        return result

    @staticmethod
    def get_random_phrase_after_request() -> str:
        """Возвращает случайную реплику из списка"""

        return choice(RANDOM_WORDS_ECHO)

    @staticmethod
    def get_adding_confirmation_str(word: str) -> str:
        """Возвращает строку с подтверждением добавления слова"""

        return Message.SET_LEARNING_WORD_STATUS.value.format(word)

    @staticmethod
    def get_learning_word_string(word: str, word_meanings: dict) -> str:
        """Возвращает строку со случайным словом и его значениями"""

        result = Message.LEARNING_WORD.value.format(word) + "\n\n"

        for meaning in word_meanings[word]:
            result += "\n" + f"_{meaning}_: {word_meanings[word][meaning]}" + "\n"

        return result

    @staticmethod
    def get_random_inspiration_phrase() -> str:
        """Возвращает случайную реплику из списка воодушевляющих фраз"""

        return choice(INSPIRATION_PHRASES)

    @staticmethod
    def get_status_changing_confirmation_str(word: str) -> str:
        """Возвращает строку с подтверждением изменения статуса слова на «Изучено»"""

        return Message.SET_LEARNED_WORD_STATUS.value.format(word)
