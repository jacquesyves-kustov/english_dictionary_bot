from .create_tables import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, ForeignKey


class Word(Base):
    __tablename__ = "word_set"

    __tableargs__ = {
        'comment': 'Список уникальных слов'
    }

    word = Column(
        Text,
        nullable=False,
        unique=True,
        primary_key=True,
        comment='Слово'
    )

    # Связываем объекты таблиц
    meanings = relationship("WordMeaning", backref="word")
    users_words = relationship("UsersWords", backref="word")

    def __repr__(self):
        return f'WORD: {self.word}'


class WordMeaning(Base):
    __tablename__ = "word_meaning"

    __tableargs__ = {
        'comment': 'Список слов со всеми употреблениями по частям речи'
    }

    word_text = Column(
        Text,
        ForeignKey('word_set.word'),
        nullable=False,
        primary_key=True
    )

    part_of_speech = Column(
        Text,
        nullable=False,
        primary_key=True,
        comment='Часть речи'
    )

    meanings = Column(
        Text,
        nullable=False,
        comment='Значение слова в данной части речи'
    )

    def __repr__(self):
        return f'WORD: {self.word_text}, PART OF SPEECH: {self.part_of_speech}, MEANING: {self.meanings}'
