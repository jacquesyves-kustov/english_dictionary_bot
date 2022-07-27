import storage
import argparse
import clients
import data_fetcher
import bot_engine
import notification_manager
from config import RMQ_NEW_WORDS_QUEUE_STR


parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Run a special container")
args = parser.parse_args()


# Инициализация таблиц в БД
if args.mode == "db":
    storage.create_database()

# Получение и отправка списка новых слов
elif args.mode == "words":
    rabbitmq_client = clients.RabbitClient(RMQ_NEW_WORDS_QUEUE_STR)
    data_fetcher.loading_new_words(rabbitmq_client)
    rabbitmq_client.__del__()

# Получение определения слов и запись их в БД
elif args.mode == "def":
    rabbitmq_client = clients.RabbitClient(RMQ_NEW_WORDS_QUEUE_STR)
    rabbitmq_client.consume(data_fetcher.parser_message_handler, RMQ_NEW_WORDS_QUEUE_STR)
    rabbitmq_client.__del__()

# Скрипт бота для взаимодействия с юзером
elif args.mode == "bot":
    bot_engine.create_bot()

# Менеджер уведомлений
elif args.mode == "notification_manager":
    notification_manager.create_manager()
