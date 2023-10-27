from src.services import contents as cntnt, web_scraping as ws
from src.database import DBManager as Manager
from typing import List, Dict
import threading


news: List[cntnt.News] = []
containers: Dict[int, List[cntnt.News]] = {}
init_news = threading.Thread(target=Manager.get_news_db, args=(news, containers))


def init_thread() -> None:
    global news, containers
    if not news:
        print("entra")
        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MÁS RAPIDO TIENEN QUE IR
        init_news.start()

        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        threading.Thread(target=_add_news_background).start()

    # SON PRUEBAS, SIRVEN PARA VER ESTOS DATOS POR CONSOLA
    # lista = Manager.loadUncheckedUsers()
    #  lista = Manager.load_new()
    #  for i in lista:
    #      print(i)

    print(f"sale {news}")
    pass


def _add_news_background() -> None:
    global news, containers
    news += ws.get_news()
    containers = ws.get_containers(news)
    pass


def get_news():
    return news


def get_containers():
    return containers
