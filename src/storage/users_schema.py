from .create_tables import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, BigInteger, ForeignKey


class User(Base):
    __tablename__ = "users"

    __tableargs__ = {
        'comment': 'Список всех уникальных пользователей'
    }

    user_id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        comment='User ID'
    )

    chat_id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        comment='Chat ID'
    )

    name = Column(
        Text,
        nullable=False,
        comment="User's first name"
    )

    # Выученные слова
    users_words = relationship("UsersWords", backref="user")

    def __repr__(self):
        return f'USER ID: {self.user_id}, USER CHAT ID: {self.chat_id}, USER NAME: {self.name}'


class UsersWords(Base):
    # Значения для прогресса работы юзера над словом
    WORD_IN_PROGRESS_MARKER = "in_progress"
    WORD_IS_LEARNED_MARKER = "is_learned"

    __tablename__ = "users_words"

    __tableargs__ = {
        'comment': 'Список слов, которые юзер выучил или учит'
    }

    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id'),
        nullable=False,
        primary_key=True
    )

    users_word = Column(
        Text,
        ForeignKey('word_set.word'),
        nullable=False,
        primary_key=True
    )

    users_word_status = Column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return f'USER ID: {self.user}, USERS WORD: {self.users_word}, WORD STATUS: {self.users_word_status}'


