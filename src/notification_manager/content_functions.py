from storage import db_session, UsersTablesHandler, WordsTablesHandler
from .content_strings import Messages


words_db = WordsTablesHandler()
users_db = UsersTablesHandler()


def generate_notification_text(user_id: int) -> str:
    """Генерирует строку текста уведомления"""

    # Получаем все слова изучаемые юзером
    users_learning_words = users_db.get_all_users_learning_words(user_id, db_session)

    # Если список изучаемых слов пуст, то напоминаем о тренировках
    if len(users_learning_words) == 0:
        return get_empty_learning_words_list_notification(user_id)

    # Если список не пуст, то генерируем большой текст из изучаемых слов и их определений
    message_text = get_default_start_notification_text(user_id)

    for word_i, word_v in enumerate(users_learning_words):
        message_text += f"{word_i + 1}) *{word_v}*!\n"
        word_meanings = words_db.get_word_meanings(word_v, db_session)

        for meaning in word_meanings[word_v]:
            message_text += "\n" + f"_{meaning}_: {word_meanings[word_v][meaning]}" + "\n"

        message_text += "\n\n"

    return message_text


def get_empty_learning_words_list_notification(telegram_user_id: int) -> str:
    """Возвращает строчку для уведомления о пустом списке изучаемых слов"""

    user_name = users_db.get_user_first_name(telegram_user_id, db_session)

    return Messages.HELLO.value.format(user_name) + " " + Messages.EMPTY_WORD_LIST.value


def get_default_start_notification_text(telegram_user_id: int) -> str:
    """Возвращает стандартную строчку начала уведомления"""

    user_name = users_db.get_user_first_name(telegram_user_id, db_session)

    return Messages.HELLO.value.format(user_name) + " " + Messages.NOTIFICATION_DEFAULT_TEXT.value
