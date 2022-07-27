from clients import RabbitClient
from time import sleep
from config import RMQ_NEW_WORDS_QUEUE_STR
from data_fetcher import get_word_definition, get_random_words_list
from storage import db_session, WordsTablesHandler


words_db = WordsTablesHandler()


def loading_new_words(rabbitmq_client: RabbitClient) -> None:
    """Логика отправки случайных слов брокеру"""

    while True:
        # Получаем список новых слов
        new_words_list = get_random_words_list()

        # Искусственно замедляем время выполнения
        sleep(5)

        # Отправляем в очередь, в случае любой ошибки - выходим из цикла и закрываем соединение
        try:
            for word in new_words_list:
                rabbitmq_client.publish(word, RMQ_NEW_WORDS_QUEUE_STR)

        except Exception:
            break


def parser_message_handler(message_body: str) -> None:
    """Логика обработки сообщений из парсера"""

    # Проверяем наличие слова в БД
    if not words_db.is_word_in_database(message_body, db_session):
        # Если слова нет в БД, то находим его значения
        new_word_meanings_dict = get_word_definition(message_body)

        if bool(new_word_meanings_dict):
            # Если их список значений не пуст, то заносим данные в БД
            words_db.add_word_into_dictionary(
                message_body,
                new_word_meanings_dict,
                db_session
            )

            print(" [DEF] Word", message_body, "has been processed!")

        else:
            print(" [DEF] Meaning dictionary", message_body, "is empty!")

    else:
        print(" [DEF] Word", message_body, "is in database!")
