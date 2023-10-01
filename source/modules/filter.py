import classes as cl
from typing import List
import re
import requests

# from modules import classes as cl


def filter_by_words(search: str, news: List[cl.News]) -> List[cl.News]:
    words = search.split(" ")
    all_news = []
    for word in words:
        all_news = all_news + _search_title(word, news) + _search_content(word, news)
    return list(set(all_news))


def _search_title(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        if re.match(word, new.get_title()):
            matches.append(new)

    return matches


def _search_content(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        if re.match(word, requests.get(new.get_url()).text):
            matches.append(new)

    return matches
