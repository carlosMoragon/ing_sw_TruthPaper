import re
from typing import List
from src.services import contents as cntnt
from src.utils import validations as vld


# FILTRO PRINCIPAL
def filter_by_words(search: str, news: List[cntnt.News]) -> List[cntnt.News]:
    words = search.lower().split(" ")
    all_news = []
    for word in words:
        if vld.validate_date(word):
            all_news += filter_by_date(search, news)
        else:
            # FILTRAR POR TÍTULO, CATEGORÍA y CONTENIDO
            all_news = (all_news +
                        _filter_by_title(word, news) +
                        filter_by_categories(word, news) +
                        _filter_by_content(word, news))

    return list(set(all_news))  # Si hay alguna noticia repetida, que se elimine y después lo converitmos en lista


def _filter_by_title(word: str, news: List[cntnt.News]) -> List[cntnt.News]:
    matches = []
    for new in news:
        # Puede que new.get_title() este devolviendo una List[str]
        if re.search(word, str(new.get_title()).lower()):
            matches.append(new)

    return matches


def _filter_by_content(word: str, news: List[cntnt.News]) -> List[cntnt.News]:
    matches = []
    for new in news:
        if re.search(word, new.get_content()):
            matches.append(new)

    return matches


def filter_by_categories(category: str, news: List[cntnt.News]) -> List[cntnt.News]:
    matches = []
    if vld.validate_date(category):
        for new in news:
            if category == str(new.get_category().lower()):
                matches.append(new)

    return matches


def filter_by_date(search: str, news: List[cntnt.News]) -> List[cntnt.News]:
    matches = []
    if vld.validate_date(search):
        for new in news:
            if search == str(new.get_date()):
                matches.append(new)

    return matches


def filter_by_container(container: int, news: List[cntnt.News]) -> List[cntnt.News]:
    matches = []
    for new in news:
        if container == new.get_container():
            matches.append(new)

    return matches
