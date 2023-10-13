from modules import classes as cl, web_scrapping as ws
from typing import List
import re


def filter_by_categories(category: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    if cl.validate_date(category):
        for new in news:
            if category == str(new.get_category().lower()):
                matches.append(new)
    return matches


def filter_by_date(search: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    if cl.validate_date(search):
        for new in news:
            if search == str(new.get_date()):
                matches.append(new)

    return matches


def filter_by_words(search: str, news: List[cl.News]) -> List[cl.News]:
    words = search.lower().split(" ")
    all_news = []
    for word in words:
        if cl.validate_date(word):
            all_news += filter_by_date(search, news)
        else:
            all_news = all_news + _search_title(word, news) + filter_by_categories(word, news)# + _search_content(word, news)
    return list(set(all_news))


def _search_title(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        # Puede que new.get_title() este devolviendo una List[str]
        if re.search(word, str(new.get_title()).lower()):
            matches.append(new)

    return matches


def _search_content(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        if re.search(word, ws.get_content(new.get_url())):
            matches.append(new)

    return matches
