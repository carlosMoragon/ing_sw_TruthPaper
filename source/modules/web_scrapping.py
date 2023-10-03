import requests
#  pip install beautifulsoup4
from bs4 import BeautifulSoup
from modules import classes as cl
# import classes as cl
from typing import List
from datetime import datetime
import os
import html


def build_news(titles, urls, imgs, owner: str) -> List[cl.News]:
    # print(f"titles.len: {len(titles)}, urls.len: {len(urls)}, imgs.len: {len(imgs)}\n")
    news = []
    for i in range(len(imgs)):
        # print(f"{titles[i]}\n")
        news.append(cl.News(titles[i], imgs[i], "", urls[i], datetime.now().strftime(f"%Y-%m-%d"), owner))

    return news


def get_content(url: str) -> str:
    web_structure = BeautifulSoup(requests.get(url).text, 'lxml')
    all_p = web_structure.find_all('p')
    text = []
    for p in all_p:
        text.append(p.text)
    return ''.join(text)


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
        a_texts = [a_tag.text.strip() for a_tag in a_tags[len(a_tags)-1]]
        titles.append(a_texts)

    # url_imgs = [article.find('img').get('src') for article in articles]
    url_imgs = []

    for article in articles:
        img_tag = article.find('img')
        if img_tag is not None:
            src = img_tag.get('src')
            if src is not None:
                url_imgs.append(src)
        else:
            url_imgs.append("./static/img/nohayfoto.avif")

    return build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='antena3noticias')


def get_lasextanews() -> List[cl.News]:

    lasexta = requests.get("https://www.lasexta.com/noticias/")
    lasexta_structure = BeautifulSoup(lasexta.text, 'lxml')

    articles = lasexta_structure.find_all('article')
    link_news = [article.find('a').get('href').strip() for article in articles]
    url_imgs = [article.find('img').get('src') for article in articles]

    titles = []
    for article in articles:
        # h2_tags = article.find_all('h2', class_='titular t3')
        h2_tags = article.find_all('h2')
        h2_texts = [h2_tag.text.strip() for h2_tag in h2_tags]
        titles.append(h2_texts)

    return build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='LaSexta')


def get_marcanews() -> List[cl.News]:
    return None


def save_html():
    urls = ["https://www.lasexta.com/noticias/", "https://www.antena3.com/noticias/"]
    day = datetime.now().strftime(f'%Y-%m-%d')
    route = ".\\almacenTemporalHTML\\"
    names = [f"{route}lasexta_{day}.html", f"{route}antena3_{day}.html"]

    for index in range(len(urls)):
        # Verificar si el archivo ya existe
        if not os.path.exists(urls[index]):
            # Definir el contenido HTML
            content_html = requests.get(urls[index]).text
            # Escribir en el fichero
            with open(names[index], "w", encoding="utf-8") as archivo:
                archivo.write(html.unescape(content_html))