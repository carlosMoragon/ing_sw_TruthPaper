import requests
#  pip install beautifulsoup4
from bs4 import BeautifulSoup
import classes as cl
from typing import List
from datetime import datetime


# Implementando el webScrapping de antena3noticias
def get_antena3news() -> List[cl.News]:
    # new = cl.News(title, image, summary, url, date, owner)
    antena3 = requests.get("https://www.antena3.com/noticias/")
    antena3_structure = BeautifulSoup(antena3.text, 'lxml')

    # Encontrar articulos
    articles = antena3_structure.findAll('article')

    # Link a la noticia
    link_news = [article.find('a').get('href').strip() for article in articles]
    titles = []
    for article in articles:
        a_tags = article.find_all('a')
        a_texts = [a_tag.text for a_tag in a_tags]
        titles.append(a_texts)

    url_imgs = [article.find('img').get('src') for article in articles]
    # print("a")
    # for url in url_imgs:
    #    print(f"{url}\n")
    # print(link_news)
    # print(titles)

    news = []
    for i in range(len(titles)):
        news.append(cl.News(titles[i][1], url_imgs[i], "", link_news[i], datetime.now().strftime(f"%Y-%m-%d"), "Antena 3 Noticias").__str__())
    # cl.News(titles, url_imgs, "", link_news, datetime.now().strftime(f"%Y-%m-%d"), "Antena 3 Noticias")
    print(news)
    return news


get_antena3news()


def get_lasextanews():

    lasexta = requests.get("https://www.lasexta.com/noticias/")
    lasexta_structure = BeautifulSoup(lasexta.text, 'lxml')