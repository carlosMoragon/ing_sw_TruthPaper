import requests
from bs4 import BeautifulSoup
from modules import classes as cl
from typing import List
from datetime import datetime
import os
import html
import glob
import re
from concurrent.futures import ThreadPoolExecutor


def _build_news(titles: List[str], urls: List[str], imgs: List[str], owner: str, date: str) -> List[cl.News]:
    news = []
    for i in range(len(urls)):
        news.append(cl.News(titles[i], imgs[i], "", urls[i], date, owner, ""))

    # zsave_content(news)
    return news


def _make_antena3news(content: str, date: str) -> List[cl.News]:

    antena3_structure = BeautifulSoup(content, 'lxml')
    articles = antena3_structure.find_all('article')

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

    return _build_news(titles=titles, urls=link_news, imgs=url_imgs, owner='antena3noticias', date=date)


def _make_lasexta_marca_news(content: str, date: str) -> List[cl.News]:

    lasexta_structure = BeautifulSoup(content, 'lxml')
    articles = lasexta_structure.find_all('article')
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
        titles.append(h2_texts)

    return _build_news(titles=[title[0] for title in titles], urls=link_news, imgs=url_imgs, owner='LaSexta', date=date)


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

    return [cl.News(titles[i][0], 'static\\img\\nytimes.png', "", link_news[i], date, "The New York Times", "") for i in range(len(link_news))]


def get_news() -> List[cl.News]:
    newspapers = {
        "antena3": _make_antena3news,
        "lasexta": _make_lasexta_marca_news,
        "marca": _make_lasexta_marca_news,
        "nytimes": _make_nytimesnews
    }
    pattern = r"./almacenTemporalHTML/*"

    htmls = glob.glob(pattern)

    news = []
    for file_name in htmls:
        with open(file_name, "r", encoding="utf-8") as archivo:
            content = archivo.read()
            search = re.search(r"(\w+)_(\d{4}-\d{2}-\d{2})\.html", file_name)
            date = search.group(2)
            name = search.group(1)
            news += newspapers[name](content, date)

    return news


def save_content(news: List[cl.News]):
    with ThreadPoolExecutor(max_workers=5) as executor:
        content = list(executor.map(get_content, [new.get_url() for new in news]))
        for i in range(len(news)):
            news[i].set_content(content[i])
    print("TERMINADO")


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


def save_html() -> None:
    urls = ["https://www.lasexta.com/noticias/", "https://www.antena3.com/noticias/", "https://www.marca.com/", "https://www.nytimes.com/international/"]
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
