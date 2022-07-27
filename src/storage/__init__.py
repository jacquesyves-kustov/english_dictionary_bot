from .dictionary_tables_interface import WordsTablesHandler
from .users_interface import UsersTablesHandler
from .create_tables import create_database, db_session


# Полное содержание пакета:

# I) Описание ДБ (.create_tables):
# Функция create_database() - инициализирует таблицы в начале программы и возвращает экземпляр сессии
#   1. Таблицы контента (.dictionary_tables_schema):
#       1а. Таблица всех уникальных слов (Word)
#       2б. Таблица значений слов по частям речи (WordMeaning)

#   2. Таблицы, описывающие юзеров (.users_schema):
#       2а. Таблица всех уникальных юзеров (User)
#       2б. Таблица слов, которые изучены/изучаются юзерами (UsersWords)


# II) Интерфейс по взаимодействую с таблицами:
#   1. Для таблиц контента (.dictionary_tables_interface):
#       1a. Функция, возвращающая значение конкретного слова - get_word_meanings()
#       1б. Функция, добавляющая новое слово и его значения в таблицы - add_word_into_dictionary()

#   2. Для таблиц юзеров (.users_interface):
#       2a. Добавление нового юзера - add_new_user()
#       2б. Функция, которая дает N новых слов для юзера - get_new_words_for_user()
#       2в. Функция, которая возвращает ВСЕ изученные юзером слова get_all_users_learned_words()
#       2г. Функция, которая возвращает ВСЕ изучаемые юзером слова - get_all_users_learning_words()
