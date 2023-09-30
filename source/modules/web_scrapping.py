import requests
#  pip install beautifulsoup4
from bs4 import BeautifulSoup
from modules import classes as cl
from typing import List
from datetime import datetime


def build_news(titles, urls, imgs, owner: str) -> List[cl.News]:
    # print(f"titles.len: {len(titles)}, urls.len: {len(urls)}, imgs.len: {len(imgs)}\n")
    news = []
    for i in range(len(titles)):
        # print(f"{titles[i]}\n")
        news.append(cl.News(titles[i], imgs[i], "", urls[i], datetime.now().strftime(f"%Y-%m-%d"), owner))

    return news


def get_antena3news() -> List[cl.News]:
    # new = cl.News(title, image, summary, url, date, owner)
    antena3 = requests.get("https://www.antena3.com/noticias/")
    antena3_structure = BeautifulSoup(antena3.text, 'lxml')

    # Encontrar articulos
    articles = antena3_structure.find_all('article')

    # Link a la noticia
    link_news = [article.find('a').get('href').strip() for article in articles]
    titles = []
    for article in articles:
        a_tags = article.find_all('a')
        a_texts = [a_tag.text for a_tag in a_tags[len(a_tags)-1]]
        titles.append(a_texts)

    url_imgs = [article.find('img').get('src') for article in articles]
    # [title[1] for title in titles]
    return build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='antena3noticias')


def get_lasextanews() -> List[cl.News]:

    lasexta = requests.get("https://www.lasexta.com/noticias/")
    lasexta_structure = BeautifulSoup(lasexta.text, 'lxml')

    articles = lasexta_structure.find_all('article')
    link_news = [article.find('a').get('href').strip() for article in articles]
    url_imgs = [article.find('img').get('src') for article in articles]

    titles = []
    for article in articles:
        h2_tags = article.find_all('h2', class_='titular t3')
        h2_texts = [h2_tag.text for h2_tag in h2_tags]
        titles.append(h2_texts)

    return build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='LaSexta')

