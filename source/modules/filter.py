# import classes as cl
<<<<<<< HEAD
=======
# import web_scrapping as ws
>>>>>>> 1965186a1491b4bc8e0ee7f0ac3fae4a14a86656
from modules import classes as cl, web_scrapping as ws
from typing import List
import re
import requests

<<<<<<< HEAD
# import web_scrapping as ws
=======

>>>>>>> 1965186a1491b4bc8e0ee7f0ac3fae4a14a86656


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
        if re.search(word, str(new.get_title())):
            matches.append(new)

    return matches


def _search_content(word: str, news: List[cl.News]) -> List[cl.News]:
    matches = []
    for new in news:
        if re.search(word, ws.get_content(new.get_url())):
            matches.append(new)

    return matches
