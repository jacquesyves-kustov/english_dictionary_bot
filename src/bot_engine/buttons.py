import telebot
from telebot import types
from .content_strings import callback_data_sep, Command, ReplyButton, InlineButton


class BotButtonsHandler:
    @staticmethod
    def create_default_reply_buttons() -> "Стандартный набор reply кнопок":
        """
        Создает стандартный набор reply кнопок

        random_btn - кнопка для получения случайного слова
        show_learning_words_btn - кнопка для получения списка изучаемых юзером слов
        """

        # Экземпляр разметки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Описываем кнопки
        random_btn = types.KeyboardButton(ReplyButton.RANDOM.value)
        show_learning_words_btn = types.KeyboardButton(ReplyButton.SHOW_LEARNING_WORDS.value)

        # Добавляем кнопки
        markup.add(random_btn, show_learning_words_btn)

        return markup

    @staticmethod
    def create_add_learning_word_inline_button(word: str, user_id: int) -> "Кнопка для добавления слова на изучение":
        """Создаем inline кнопку, чтобы юзер мог добавить его на изучение"""

        keyboard = telebot.types.InlineKeyboardMarkup()

        button = telebot.types.InlineKeyboardButton(
            InlineButton.ADD_WORD_INTO_ROTATION.value,
            callback_data=Command.ADD_NEW_WORD.value + callback_data_sep + word + callback_data_sep + str(user_id)
        )

        keyboard.row(button)

        return keyboard

    @staticmethod
    def create_delete_learning_word_inline_button(word: str, user_id: int) -> "Кнопка для удаления слова с изучения":
        """Создаем inline кнопку, чтобы юзер мог удалить слово"""

        keyboard = telebot.types.InlineKeyboardMarkup()

        button = telebot.types.InlineKeyboardButton(
            InlineButton.SET_LEARNED_STATUS.value,
            callback_data=Command.SET_LEARNED_STATUS.value + callback_data_sep + word + callback_data_sep + str(user_id)
        )

        keyboard.row(button)

        return keyboard
