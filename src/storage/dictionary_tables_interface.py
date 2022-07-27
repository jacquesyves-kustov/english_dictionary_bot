import sqlalchemy.orm.session
import random
from sqlalchemy.exc import IntegrityError
from .dictionary_tables_schema import Word, WordMeaning


class WordsTablesHandler:
    @staticmethod
    def add_word_into_dictionary(word: str, word_meanings: dict, session: sqlalchemy.orm.Session) -> None:
        """Функция, которая добавляет в таблицу новое слово"""

        # Создаем новый объект для таблицы уникальных слов
        new_word = Word(word=word)

        for new_part_of_speech in word_meanings:
            # Собираем список значений в строку
            new_meaning = " ".join(word_meanings[new_part_of_speech])

            # Создаем новый объект для таблицы значений
            new_word_meanings = WordMeaning(
                part_of_speech=new_part_of_speech,
                meanings=new_meaning
            )

            # Связываем новый объект таблицы значений с новым объектом таблицы уникальных слов
            new_word.meanings.append(new_word_meanings)

        try:
            # Добавляем получившийся на отправку
            session.add(new_word)

            # Отправляем новые данные в таблицу
            session.commit()

        except IntegrityError:
            # В случае если слово оказалось в БД, то вызываем метод rollback(), чтобы можно было делать новые транзакции
            session.rollback()

    @staticmethod
    def get_word_meanings(requested_word: str, session: sqlalchemy.orm.Session) -> "Словарь значений по частям речи":
        """Функция для получения словаря значений переданного слова по частям речи"""

        # Находим значения запрашиваемого слова в таблице
        result = session.query(WordMeaning).filter(WordMeaning.word_text == requested_word).all()

        # Создаем на основе полученных данных словарь
        result_dict = dict()

        for row in result:
            result_dict[row.part_of_speech] = row.meanings

        return {requested_word: result_dict}

    @staticmethod
    def is_word_in_database(requested_word: str, session: sqlalchemy.orm.Session) -> "True, если слово есть в БД":
        """Проверяем, находится ли передаваемое слово в таблице уникальных слов"""

        result = session.query(Word).filter(Word.word == requested_word).first()

        return result is not None

    @staticmethod
    def get_random_word_from_database(session: sqlalchemy.orm.Session):
        """Возвращает одно случайное слово из таблицы уникальных слов"""

        rand = random.randrange(0, session.query(Word).count())
        row = session.query(Word)[rand]

        return row.word

    @staticmethod
    def get_random_words_from_database(words_number: int, session: sqlalchemy.orm.Session):
        """Возвращает список из words_number случайных слов из таблицы уникальных слов"""

        random_words = list()

        for it in range(words_number):
            rand = random.randrange(0, session.query(Word).count())
            random_words.append(session.query(Word)[rand].word)

        return random_words
