import requests
from time import sleep
from bs4 import BeautifulSoup


PART_OF_SPEECH_DICT = {
    "n.": "Noun",
    "pl.n.": "Plural Noun",
    "v.": "Verb",
    "tr.v.": "Transitive Verb",
    "intr.v.": "Intransitive Verb",
    "intr. & tr.v.": "Intransitive and Transitive Verb",
    "tr. & intr.v.": "Transitive and Intransitive Verb",
    "adv.": "Adverb",
    "adj.": "Adjective",
    "prep.": "Preposition",
    "abbr.": "Abbreviation",
    "conj.": "Conjunction",
    "pron.": "Pronoun",
    "?": "Meaning"
}


def get_soup_instance(url: str) -> "Экземпляр bs4":
    """Получаем экземпляр bs4 с таймаутом при неудаче"""

    while True:
        try:
            # Если сайт доступен, то делаем экземпляр bs4 и выходим из цикла
            html = requests.get(url).content
            soup = BeautifulSoup(html, "lxml")

            break

        except requests.exceptions.RequestException:
            # Если не сайт не доступен, ждем минуту и пробуем снова
            print(" [NEW WORDS PARSER] The connection is lost!")
            sleep(60)

    return soup


def get_random_words_list() -> "Список новых (случайных слов)":
    # Получаем экземпляр bs4 страницы, на которой лежат рандомные слова
    soup = get_soup_instance("https://www.thefreedictionary.com/dictionary.htm")

    # Обращаемся ко второму элементу блока "CustHPBlock box", где: 'ul' - список, 'a' - элементы списка
    soup = soup.find_all("div", {"class": "CustHpBlock box"})
    random_words = [child.string for child in soup[1].find("ul").find_all('a')]

    return random_words


def get_word_definition(word: str) -> "Словарь значения слова по частям речи":
    """Собираем значения передаваемого слова"""

    # Создаем пустой словарь значений
    # KEY: VALUE
    # "Часть речи": ["Значение1", "Значение2"]
    temp_dict = dict()

    # Переходим по ссылке к статье об этом слове
    definition = get_soup_instance("https://www.thefreedictionary.com/" + word).find("div", {"id": "Definition"})

    # Для каждой части речи собираем значения:
    # - у слова в одной части речи может быть одно значение: блок <div class="ds-single">
    # - у слова в одной части речи может быть несколько значений: блок <div class="ds-list">
    # - у слова в одной части речи в одном значении может быть список подзначений: блок <div class="sds-list">

    for part in definition.find_all("div", {"class": "pseg"}):
        meaning_lst = []  # Пустой список значений - будет заполняться во время парсинга

        # Если у слова одно значение и оно не является ссылкой на другое слово, то сохраним его
        if part.find("div", {"class": "ds-single"}) is not None and part.find("div", {"class", "ds-single"}).find(
                'a') is None:
            meaning_str = part.find("div", {"class", "ds-single"}).get_text()

            # Если в строке есть лишние пробелы в начале и в конце, то мы их почистим
            meaning_str = meaning_str.strip()

            # Добавляем значение в список
            meaning_lst.append(meaning_str)

        # Если у слова несколько значений
        elif part.find_all("div", {"class": "ds-list"}) is not None:
            # Для каждого значения
            for meaning in part.find_all("div", {"class": "ds-list"}):
                # Если значение является ссылкой на другую статью, то пропускаем
                if meaning.find('a') is not None:
                    continue

                # Если значение имеет список подзначений
                if meaning.find("div", {"class": "sds-list"}) is not None:
                    # Для каждого подзначения
                    for sub_meaning in meaning.find_all("div", {"class": "sds-list"}):
                        # Добавляем в строку каждое значение, удалив "N. " в начале
                        meaning_str = sub_meaning.get_text()[3:]

                        # Если в строке есть лишние пробелы в начале и в конце, то мы их почистим
                        meaning_str = meaning_str.strip()

                        # Добавляем подзначение в список значений
                        meaning_lst.append(meaning_str)
                else:
                    # Если подзначений нет, то просто сохраняем значение в строку
                    meaning_str = meaning.get_text()

                    # Из-за ссылок нумерация может сбиться, поэтому удаляем "N. " в начале каждого значения
                    if meaning_str[0].isdigit():
                        meaning_str = meaning_str[3:]

                    # Если в строке есть лишние пробелы в начале и в конце, то мы их почистим
                    meaning_str = meaning_str.strip()

                    # Удаляем пробелы и добавляем обработанное значение в список значений
                    meaning_lst.append(meaning_str)

        # Если не было найдено корректных значений за частью речи, то оно не будет добавлено
        if len(meaning_lst) == 0:
            continue
        else:
            # Если часть речи не было указана, то сохраним вопросительный знак
            key = "?" if (part.find('i') is None or part.find('i').get_text() == "") else part.find('i').get_text()

            # Обращаемся к пререквизиту, чтобы получить удобную для чтения часть речи
            # Если такого ключа нет, то ключом выступит вопросительный знак
            key = PART_OF_SPEECH_DICT.get(key, key)

            # Во временный словарь сохраняем получившийся список значений под ключом части речи
            temp_dict[key] = meaning_lst

    # Если словарь значений пуст, то слово не будет добавлено. В обратном случае temp_dict все еще пуст
    return temp_dict
