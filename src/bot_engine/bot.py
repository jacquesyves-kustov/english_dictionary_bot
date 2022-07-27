import telebot
from config import TELEGRAM_TOKEN
from .buttons import BotButtonsHandler
from .content_strings import callback_data_sep, Command, ReplyButton, Message
from .content_functions import MessageHandler
from storage import db_session, UsersTablesHandler, WordsTablesHandler


def create_bot():
    """Создает бота"""

    # Экземпляр бота
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    # Экземпляры статических классов
    msg = MessageHandler()
    btn = BotButtonsHandler()
    users_db = UsersTablesHandler()
    words_db = WordsTablesHandler()

    @bot.message_handler(commands=[Command.START.value])
    def send_welcome(message):
        """
        Обработка команды /start

        Добавление данных о юзере в БД и вывод приветственных сообщений
        """

        # Получаем айди и имя юзера
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.first_name

        # Отправляем в базу айди и имя
        users_db.add_new_user(user_id, chat_id, user_name, db_session)

        # Выводим сообщения
        bot.send_message(
            chat_id,
            msg.get_hello_string(user_name),
            parse_mode="Markdown"
        )

        bot.send_message(
            chat_id,
            Message.TUTORIAL.value,
            reply_markup=btn.create_default_reply_buttons(),
            parse_mode="Markdown"
        )

    @bot.message_handler(content_types='text')
    def message_reply(message):
        """Обработка кнопок, которые отправляют текстовые сообщения"""

        if message.text == ReplyButton.RANDOM.value:
            # Получаем случайное слово из БД
            random_word = words_db.get_random_word_from_database(db_session)

            # Формируем строку для сообщения
            message_text = msg.get_random_word_string(random_word, words_db.get_word_meanings(random_word, db_session))

            # Выводим сообщения
            bot.send_message(
                message.chat.id,
                message_text,
                reply_markup=btn.create_add_learning_word_inline_button(random_word, message.from_user.id),
                parse_mode="Markdown"
            )

            # Случайная фраза
            bot.send_message(
                message.chat.id,
                msg.get_random_phrase_after_request(),
                reply_markup=btn.create_default_reply_buttons(),
                parse_mode="Markdown"
            )

        elif message.text == ReplyButton.SHOW_LEARNING_WORDS.value:
            # Получаем список слов, изучаемых юзером
            users_learning_words = users_db.get_all_users_learning_words(message.from_user.id, db_session)

            # Выводим каждое слово и его значения отдельными сообщениями
            for word in users_learning_words:
                # Формируем строку для сообщения
                message_text = msg.get_learning_word_string(word, words_db.get_word_meanings(word, db_session))

                # Выводим сообщения
                bot.send_message(
                    message.chat.id,
                    message_text,
                    reply_markup=btn.create_delete_learning_word_inline_button(word, message.from_user.id),
                    parse_mode="Markdown"
                )

            # После отправки всех изучаемых слов выводим стандартный интерфейс
            # и сообщение в зависимости от количества слов в списке
            bot.send_message(
                message.chat.id,
                msg.get_random_inspiration_phrase() if bool(len(users_learning_words)) else Message.EMPTY_LEARNING_WORDS.value,
                reply_markup=btn.create_default_reply_buttons(),
                parse_mode="Markdown"
            )

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        """
        Обработка inline кнопок

        call.data.split(callback_data_sep)[0] - команда
        call.data.split(callback_data_sep)[1] - данные для передачи хэндлеру
        call.data.split(callback_data_sep)[2] - user_id
        ...

        """

        if call.data.split(callback_data_sep)[0] == Command.ADD_NEW_WORD.value:
            # Добавляем слово в таблицу users_words
            users_db.add_new_learning_word(
                call.data.split(callback_data_sep)[2],
                call.data.split(callback_data_sep)[1],
                db_session
            )

            # Подтверждаем добавление
            bot.send_message(
                call.message.chat.id,
                msg.get_adding_confirmation_str(call.data.split(callback_data_sep)[1]),
                reply_markup=btn.create_default_reply_buttons(),
                parse_mode="Markdown"
            )

        elif call.data.split(callback_data_sep)[0] == Command.SET_LEARNED_STATUS.value:
            # Меняем статус изучения слова в БД
            users_db.add_new_learned_word(
                call.data.split(callback_data_sep)[2],
                call.data.split(callback_data_sep)[1],
                db_session
            )

            # Подтверждаем изменение статуса
            bot.send_message(
                call.message.chat.id,
                msg.get_status_changing_confirmation_str(call.data.split(callback_data_sep)[1]),
                reply_markup=btn.create_default_reply_buttons(),
                parse_mode="Markdown"
            )

    bot.infinity_polling()
