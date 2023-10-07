import requests
#  pip install beautifulsoup4
from bs4 import BeautifulSoup
from modules import classes as cl
# import classes as cl
from typing import List
from datetime import datetime
import os
import html
import glob
import re


def _build_news(titles, urls, imgs, owner: str, date: str) -> List[cl.News]:
    news = []
    for i in range(len(urls)):
        news.append(cl.News(titles[i][0], imgs[i], "", urls[i], date, owner))

    return news


def get_content(url: str) -> str:
    web_structure = BeautifulSoup(requests.get(url).text, 'lxml')
    all_p = web_structure.find_all('p')
    text = []
    for p in all_p:
        text.append(p.text)
    return ''.join(text)


def _make_antena3news(content : str, date: str) -> List[cl.News]:
    """
    # new = cl.News(title, image, summary, url, date, owner)
    antena3 = requests.get("https://www.antena3.com/noticias/")
    """
    antena3_structure = BeautifulSoup(content, 'lxml')

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
            url_imgs.append("static\\img\\no_image.jpg")

    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='antena3noticias', date=date)


def _make_lasextanews(content : str, date: str) -> List[cl.News]:

    # lasexta = requests.get("https://www.lasexta.com/noticias/")
    lasexta_structure = BeautifulSoup(content, 'lxml')

    articles = lasexta_structure.find_all('article')
    link_news = [article.find('a').get('href').strip() for article in articles]
    url_imgs = [article.find('img').get('src') for article in articles]

    titles = []
    for article in articles:
        # h2_tags = article.find_all('h2', class_='titular t3')
        h2_tags = article.find_all('h2')
        h2_texts = [h2_tag.text.strip() for h2_tag in h2_tags]
        titles.append(h2_texts)

    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='LaSexta', date=date)


def _make_marcanews(content: str, date: str) -> List[cl.News]:
    marca_structure = BeautifulSoup(content, 'lxml')

    articles = marca_structure.find_all('article')
    link_news = [article.find('a').get('href').strip() for article in articles]
    url_imgs = [article.find('img').get('src') for article in articles]

    titles = []
    for article in articles:
        h2_tags = article.find_all('h2')
        h2_texts = [h2_tag.text.strip() for h2_tag in h2_tags]
        titles.append(h2_texts)
    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='LaSexta', date=date)


def _make_nytimesnews(content: str, date: str) -> List[cl.News]:

    nytimes_structure = BeautifulSoup(content, 'lxml')

    articles = nytimes_structure.find_all('section', class_='story-wrapper')
    # link_news = [article.find('a').get('href').strip() for article in articles]
    link_news = []

    for article in articles:
        img_tag = article.find('a')
        if img_tag is not None:
            href = img_tag.get('href')
            if href is not None:
                link_news.append(href)

    titles = []
    for article in articles:
        h3_tags = article.find_all('h3')
        h3_texts = [h3_tag.text.strip() for h3_tag in h3_tags]
        if h3_texts:
            titles.append(h3_texts)

    return [cl.News(titles[i][0], 'static\\img\\nytimes.png', "", link_news[i], date, "The New York Times") for i in range(len(link_news))]

    # return _build_news(titles=titles, urls=link_news, imgs='static\\img\\nytimes.png', owner='The New York Times', date=date)


def get_news() -> List[cl.News]:
    newspapers = {
        "antena3": _make_antena3news,
        "lasexta": _make_lasextanews,
        "marca": _make_marcanews,
        "nytimes": _make_nytimesnews
    }
    # Define el patrón de nombres de archivo como una cadena cruda
    pattern = r"./almacenTemporalHTML/*"

    # Obtiene una lista de todos los archivos que coinciden con el patrón en el directorio actual
    htmls = glob.glob(pattern)

    # Ahora puedes iterar sobre la lista de archivos y leer su contenido
    news = []
    for file_name in htmls:
        with open(file_name, "r", encoding="utf-8") as archivo:
            content = archivo.read()
            search = re.search(r"(\w+)_(\d{4}-\d{2}-\d{2})\.html", file_name)
            date = search.group(2)
            name = search.group(1)
            news += newspapers[name](content, date)
            """
            if re.search(r"antena3", name):
                print("match antena3")
                news = news + _make_antena3news(content, date)
            elif re.search(r"lasexta", name):
                print("match lasexta")
                news = news + _make_lasextanews(content, date)
            elif re.search(r"marca", name):
                print("match marca")
                news = news + _make_marcanews(content, date)
            elif re.search(r"nytimes", name):
                print("match nytimes")
                # news = news + _make_nytimesnews(content, date)
            else:
                print("NOT FOUND")
            """
    return news


def save_html() -> None:
    urls = ["https://www.lasexta.com/noticias/", "https://www.antena3.com/noticias/", "https://www.marca.com/", "https://www.nytimes.com/international/"]
    day = datetime.now().strftime(f'%Y-%m-%d')
    route = ".\\almacenTemporalHTML\\"
    pattern = r'.(\w+).com'
    newspapers_names = [re.search(pattern, url).group(1) for url in urls]
    names = [f"{route}{newspaper_name}_{day}.html" for newspaper_name in newspapers_names]

    for index in range(len(urls)):
        # Verificar si el archivo ya existe
        if not os.path.exists(urls[index]):
            # Definir el contenido HTML
            content_html = requests.get(urls[index]).text
            # Escribir en el fichero
            with open(names[index], "w", encoding="utf-8") as archivo:
                archivo.write(html.unescape(content_html))

