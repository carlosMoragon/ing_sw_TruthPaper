import requests
from bs4 import BeautifulSoup
from modules import classes as cl
from typing import List, Dict
from datetime import datetime
import os
import html
#import glob
import re
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import threading


def _build_news(titles: List[str], urls: List[str], imgs: List[str], owner: str, date: str, category: str) -> List[cl.News]:
    news = []

    for i in range(len(urls)):
        news.append(cl.News(titles[i], imgs[i], "", urls[i], [], date, owner, "", category))

    return news


# --- MAKE'S ---
def _make_antena3news(structure: BeautifulSoup, category: str, date: str) -> List[cl.News]:

    articles = structure.find_all('article')

    link_news = [article.find('a').get('href').strip() for article in articles]

    titles = []
    for article in articles:
        a_tags = article.find_all('a')
        a_texts = [a_tag.text.strip() for a_tag in a_tags[len(a_tags)-1]]
        titles.append(a_texts[0])

    url_imgs = []
    for article in articles:
        img_tag = article.find('img')
        if img_tag is not None:
            src = img_tag.get('src')
            if src is not None:
                url_imgs.append(src)
        else:
            url_imgs.append("static\\img\\no_image.jpg")

    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='antena3noticias', date=date, category=category)


def _make_lasexta_marca_news(structure: BeautifulSoup, category: str, date: str, owner: str) -> List[cl.News]:

    articles = structure.find_all('article')
    link_news = [article.find('a').get('href').strip() for article in articles]
    url_imgs = []
    for article in articles:
        img_tag = article.find('img')
        if img_tag is not None:
            src = img_tag.get('src')
            if src is not None:
                url_imgs.append(src)
        else:
            url_imgs.append("static\\img\\no_image.jpg")
    titles = []
    for article in articles:
        h2_tags = article.find_all('h2')
        h2_texts = [h2_tag.text.strip() for h2_tag in h2_tags]
        titles.extend(h2_texts)

    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner=owner, date=date, category=category)


def _make_nytimesnews(structure: BeautifulSoup, category: str, date: str) -> List[cl.News]:

    articles = structure.find_all('section', class_='story-wrapper')
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

    return [cl.News(titles[i][0], 'static\\img\\nytimes.png', "", link_news[i], [], date, "The New York Times", "", category) for i in range(len(link_news))]


# --- CATEGORIES ---
def _category_antena3(structure: BeautifulSoup) -> List[cl.News]:
    categories = structure.find_all('li', 'menu-main__item menu-main__item--level2')
    a_tags = [category.find('a') for category in categories]
    urls = [a_tag.get('href').strip() for a_tag in a_tags]
    names = [a_tag.text.strip() for a_tag in a_tags]

    sol = []
    date = datetime.now().strftime(f'%Y-%m-%d')

    for i in range(len(urls)):
        sol += _make_antena3news(BeautifulSoup(requests.get(urls[i]).text, 'lxml'), names[i], date)
    return sol


def _category_lasexta(structure: BeautifulSoup) -> List[cl.News]:
    categories = structure.find('div', class_= "wrapper_links")
    a_tags = categories.find_all('a')
    urls = [a_tag.get('href').strip() for a_tag in a_tags]
    names = [a_tag.text.strip() for a_tag in a_tags]

    sol = []
    date = datetime.now().strftime(f'%Y-%m-%d')
    for i in range(len(urls)):
        sol += _make_lasexta_marca_news(BeautifulSoup(requests.get(urls[i]).text, 'lxml'), names[i], date, "lasexta")
    return sol


def _category_marca(structure: BeautifulSoup) -> List[cl.News]:
    lu = structure.find('lu', 'main-nav-tabs main-second-menu')
    if lu is not None:
        categories = lu.find_all('li')[:-2]
    else:
        return []

    a_tags = [category.find('a') for category in categories]
    urls = [a_tag.get('href').strip() for a_tag in a_tags]
    names = [a_tag.text.strip() for a_tag in a_tags]

    sol = []
    date = datetime.now().strftime(f'%Y-%m-%d')

    for i in range(len(urls)):
        sol += _make_lasexta_marca_news(BeautifulSoup(requests.get(urls[i]).text, 'lxml'), names[i], date, "marca")
    return sol


def _category_nytimes(structure: BeautifulSoup) -> List[cl.News]:
    categories = structure.find_all('lu', 'css-397oyn')
    a_tags = [category.find('a') for category in categories]
    urls = [a_tag.get('href').strip() for a_tag in a_tags]
    names = [a_tag.text.strip() for a_tag in a_tags]

    sol = []
    date = datetime.now().strftime(f'%Y-%m-%d')

    for i in range(len(urls)):
        sol += _make_nytimesnews(BeautifulSoup(requests.get(urls[i]).text, 'lxml'), names[i], date)
    return sol


# --- GETS ---
def get_nytimes() -> List[cl.News]:
    structure = BeautifulSoup(requests.get("https://www.nytimes.com/international/").text, 'lxml')
    return _category_nytimes(structure) + _make_nytimesnews(structure, "general", datetime.now().strftime(f'%Y-%m-%d'))


def get_antena3() -> List[cl.News]:
    antena3_structure = BeautifulSoup(requests.get("https://www.antena3.com/noticias/").text, 'lxml')

    return _category_antena3(antena3_structure) + _make_antena3news(antena3_structure, "general", datetime.now().strftime(f'%Y-%m-%d'))


def get_lasexta_marca() -> List[cl.News]:
    lasexta_structure = BeautifulSoup(requests.get("https://www.lasexta.com/noticias/").text, 'lxml')
    marca_structure = BeautifulSoup(requests.get("https://www.marca.com/").text, 'lxml')
    return (_category_lasexta(lasexta_structure) +
            _make_lasexta_marca_news(lasexta_structure, "general", datetime.now().strftime(f'%Y-%m-%d'), "lasexta") +
            _category_marca(marca_structure) +
            _make_lasexta_marca_news(marca_structure, "general", datetime.now().strftime(f'%Y-%m-%d'), "marca")
            )


def get_news() -> List[cl.News]:
    news = get_antena3() + get_lasexta_marca() + get_nytimes()
    # EMPEZAR A AÑADIR EL CONTENDIDO A LAS NOTICIAS
    threading.Thread(target=add_content(news)).start()
    return news


def get_content(url: str) -> str:
    try:
        response = requests.get(url)
        web_structure = BeautifulSoup(response.text, 'lxml')
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (código de estado 200)
        all_p = web_structure.find_all('p')
        text = []
        for p in all_p:
            text.append(p.text)
        return ''.join(text)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener {url}: {e}")
        return ""


# --- ADD'S ---
# PARA IR AÑADIENDO EL CONTENIDO DE CADA NOTICIA ( ES MUY COSTOSO EN TIEMPO POR TODOS LOS REQUESTS) POR ESO THREADS
def add_content(news: List[cl.News]):
    with ThreadPoolExecutor(max_workers=5) as executor:
        content = list(executor.map(get_content, [new.get_url() for new in news]))
        for i in range(len(news)):
            news[i].set_content(str(content[i]))


"""
def save_html(urls: List[str]) -> None:
    day = datetime.now().strftime(f'%Y-%m-%d')
    route = ".\\almacenTemporalHTML\\"
    pattern = r'.(\w+).com'
    newspapers_names = [re.search(pattern, url).group(1) for url in urls]
    names = [f"{route}{newspaper_name}_{day}.html" for newspaper_name in newspapers_names]

    for index in range(len(urls)):
        if not os.path.exists(urls[index]):
            content_html = requests.get(urls[index]).text
            with open(names[index], "w", encoding="utf-8") as archivo:
                archivo.write(html.unescape(content_html))

"""