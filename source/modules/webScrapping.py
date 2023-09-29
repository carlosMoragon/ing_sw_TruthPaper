import requests
#  pip install beautifulsoup4
from bs4 import BeautifulSoup
import classes as cl
from typing import List
# Implementando el webScrapping de antena3noticias
def get_antena3news() -> List[cl.News]:
    # new = cl.News("title", "images", "resumen", "url", "comentarios", "fecha", 1, "owner")
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
    #print("a")
    for url in url_imgs:
        print(f"{url}\n")
    #print(link_news)
    #print(titles)

    return None

get_antena3news()