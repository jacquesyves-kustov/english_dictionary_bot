import sqlalchemy.orm.session
from sqlalchemy.exc import IntegrityError
from .users_schema import User, UsersWords
from .dictionary_tables_schema import Word


class UsersTablesHandler:
    @staticmethod
    def add_new_user(user_tg_id: int, chat_tg_id: int, user_tg_name: str, session: sqlalchemy.orm.Session) -> None:
        """Функция, которая добавляет в таблицу нового юзера"""

        # Создаем новый объект для таблицы уникальных юзеров
        new_user = User(
            user_id=user_tg_id,
            chat_id=chat_tg_id,
            name=user_tg_name
        )

        try:
            # Добавляем получившийся объект на отправку
            session.add(new_user)

            # Отправляем новые данные в таблицу
            session.commit()

        except IntegrityError:
            # В случае если данные были в БД, то вызываем метод rollback(), чтобы можно было делать новые транзакции
            session.rollback()

    @staticmethod
    def add_new_learning_word(telegram_user_id: int, new_word: str, session: sqlalchemy.orm.Session) -> None:
        """Функция, которая добавляет слово в список слов, изучаемых юзером"""

        new_users_word = UsersWords(
                user_id=telegram_user_id,
                users_word=new_word,
                users_word_status=UsersWords.WORD_IN_PROGRESS_MARKER
        )

        session.add(new_users_word)

        session.commit()

    @staticmethod
    def add_new_learned_word(telegram_user_id: int, learned_word: str, session: sqlalchemy.orm.Session) -> None:
        """Функция, которая отмечает, что слово было изучено юзером"""

        # Находим запрашиваемое слово
        requested_word = session.query(
            UsersWords
        ).filter(
            UsersWords.user_id == telegram_user_id
        ).filter(
            UsersWords.users_word == learned_word
        ).first()

        # Изменяем флаг
        requested_word.users_word_status = UsersWords.WORD_IS_LEARNED_MARKER

        session.commit()

    @staticmethod
    def get_user_first_name(tg_user_id: int, session: sqlalchemy.orm.Session) -> str:
        """Возвращает имя пользователя из БД по id"""

        result = session.query(User).filter(tg_user_id == User.user_id).first()

        return result.name

    @staticmethod
    def get_all_users_learned_words(telegram_user_id: int, session: sqlalchemy.orm.Session) -> list:
        """Функция, которая возвращает все слова выученные юзером"""

        result = session.query(
            UsersWords
        ).filter(
            telegram_user_id == UsersWords.user_id
        ).filter(
            UsersWords.users_word_status == UsersWords.WORD_IS_LEARNED_MARKER
        ).all()

        return [row.word for row in result]

    @staticmethod
    def get_all_users_learning_words(telegram_user_id: int, session: sqlalchemy.orm.Session) -> list:
        """Функция, которая возвращает все слова изучаемые юзером"""

        result = session.query(
            UsersWords
        ).filter(
            telegram_user_id == UsersWords.user_id
        ).filter(
            UsersWords.users_word_status == UsersWords.WORD_IN_PROGRESS_MARKER
        ).all()

        return [row.word.word for row in result]

    @staticmethod
    def get_new_words_for_user(telegram_user_id: int, session: sqlalchemy.orm.Session, new_words_number: int = 10) -> list:
        """Функция, возвращающая N новых для юзера слов"""

        # Находим все слова, которые юзер учит или выучил
        user_learns = session.query(UsersWords.users_word).filter(UsersWords.user_id == telegram_user_id)

        # Делаем исключение
        result = session.query(Word).filter(~Word.word.in_(user_learns)).limit(new_words_number).all()

        return [row.word for row in result]
