# import classes as cl
from modules import classes as cl, web_scrapping as ws
from typing import List
import re
import requests

# import web_scrapping as ws


def filter_by_words(search: str, news: List[cl.News]) -> List[cl.News]:
    words = search.split(" ")
    all_news = []
    for word in words:
        all_news = all_news + _search_title(word, news) + _search_content(word, news)
    return list(set(all_news))


def _search_title(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        # Puede que new.get_title() este devolviendo una List[str]
        if re.match(r'{}'.format(word), new.get_title()):
            matches.append(new)

    return matches


def _search_content(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        if re.match(r'{}'.format(word), requests.get(new.get_url()).text.strip()):
            matches.append(new)

    return matches


lista = filter_by_words("a", ws.get_lasextanews() + ws.get_antena3news())
if lista:
    print("Lista no vacia\n")
    print(lista)
else:
    print("lista vacia")

