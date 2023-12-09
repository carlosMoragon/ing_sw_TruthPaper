import requests
from bs4 import BeautifulSoup
from modules import classes as cl
from typing import List, Dict
from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import threading
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from database import DBManager as manager
from modules import entitymappers # import load_news, get_last_container_id

# Para que no se esté descargando todo el rato si está instalado
def isInstaled():
    try:
        nltk.data.find('tokenizers/punkt')
        return True
    except LookupError:
        return False

if not isInstaled():
    nltk.download('punkt')

# INICIO DE LA FUNCIONALIDAD


def get_news_db(app, news, container):
    with app.app_context():
        print("entra")
        news.extend(entitymappers.New.load_news())
        container.update(split_by_container(news))


def add_new_container(news: List[cl.News], app) -> List[cl.News]:
    # Lista de noticias
    news_content = [new.get_content() for new in news]

    # Crear un vectorizador TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    # Aplicar TF-IDF a las noticias
    tfidf_matrix = tfidf_vectorizer.fit_transform(news_content)

    # Calcular la similitud coseno entre las noticias
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Establecer un umbral de similitud (ajusta según tus necesidades)
    threshold = 0.7

    # Encontrar noticias relacionadas y asignarles un contenedor
    # 
    n_cont = (entitymappers.Container.get_last_container_id(app)) + 1
    print(f"asldkfjalsdjkfla: {n_cont}")
    for i in range(len(news)):
        for j in range(i + 1, len(news)):
            if cosine_similarities[i][j] >= threshold:
                if news[i].get_container_id() != -1:
                    news[j].set_container_id(news[i].get_container_id())
                elif news[j].get_container_id() != -1:
                    news[i].set_container_id(news[j].get_container_id())
                else:
                    news[i].set_container_id(n_cont)
                    news[j].set_container_id(n_cont)
                    n_cont += 1
            else:
                if news[i].get_container_id() == -1:
                    news[i].set_container_id(n_cont)
                    n_cont += 1
                if news[j].get_container_id() == -1:
                    news[j].set_container_id(n_cont)
                    n_cont += 1

    return news


def split_by_container(news: List[cl.News]) -> Dict[int, List[cl.News]]:
    containers: Dict[int, List[str]] = defaultdict(list)
    for new in news:
        if new.get_container_id() in containers:
            containers[new.get_container_id()].append(new)
        else:
            containers[new.get_container_id()] = [new]
    return containers


def get_news() -> List[cl.News]:

    news = []
    print("entra en get_news")
    for owner in ["antena3", "marca", "lasexta"]:# , "nytimes"]:
        news += NewsBuilder(owner).get_news()
        print(len(news))
    
    
    # EMPEZAR A AÑADIR EL CONTENDIDO A LAS NOTICIAS
    threading.Thread(target=add_content(news)).start()
    print("sale de get_news")
    return news


def get_containers(news: List[cl.News], app) -> Dict[int, List[cl.News]]:
    return split_by_container(add_new_container(news, app))

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
        print("entra en add_content")
#        content = list(executor.map(get_content, [new.get_url() for new in news]))
        content = list(executor.map(get_content, [new.get_url() if hasattr(new, 'get_url') else None for new in news]))
        print("aaaaaaaaaaaaa")
        for i in range(len(news)):
            
            news[i].set_content(re.sub(r'[^\x00-\x7F]+', '', str(content[i])))
    
        print("terminado")


# Encapsula la optención de noticias por WebScrapping
class NewsBuilder:
    def __init__(self, owner: str):

        url_general_by_type = {
            "antena3": "https://www.antena3.com/noticias/",
            "marca": "https://www.marca.com/",
            "lasexta": "https://www.lasexta.com/noticias/",
            "nytimes": "https://www.nytimes.com/international/"
        }

        tags_class_by_owner = {
            "antena3" : {"tag": "article", "class" : None},
            "marca" : {"tag": "article", "class" : None},
            "lasexta" : {"tag": "article", "class" : None},
            "nytimes" : {"tag": "section", "class" : "story-wrapper"}
        }

        tags_class_to_categorize = {
            "antena3" : {"tag": "li", "class" : 'menu-main__item menu-main__item--level2'},
            "marca" : {"tag": "lu", "class" : 'main-nav-tabs main-second-menu'},
            "lasexta" : {"tag": "div", "class" : "wrapper_links"},
            "nytimes" : {"tag": 'lu', "class" : 'css-397oyn'}
        }

        tags_title = {
            "antena3" : "a",
            "marca" : "h2",
            "lasexta" : "h2",
            "nytimes" : "a"
        }

        self.owner = owner
        self.general_url = url_general_by_type[owner]
        self.news = []
        self.date = datetime.now().strftime(f'%Y-%m-%d')
        self.tag = tags_class_by_owner[owner]["tag"]
        self._class = tags_class_by_owner[owner]["class"]
        self.tag_to_categorize = tags_class_to_categorize[owner]["tag"]
        self.class_to_categorize = tags_class_to_categorize[owner]["class"]
        self.tag_title = tags_title[owner]
        

    # El único método que se debe utilizar
    def get_news(self):
        structure = BeautifulSoup(requests.get(self.general_url).text, 'lxml')
        self._make_categories_news(structure)
        self._make_news(structure, "general")
        return self.news
    

    def _get_urls(self, articles) -> List[str]:
        urls = []
        for article in articles:
            img_tag = article.find('a')
            if img_tag is not None:
                href = img_tag.get('href')
                if href is not None:
                    urls.append(href)
        
        return urls


    def _get_titles(self, articles) -> List[str]:
        titles = []
        for article in articles:
            title_tags = article.find_all(self.tag_title)
            texts = [title_tag.text.strip() for title_tag in title_tags]
            if texts:
                titles.append(texts)
        
        return titles
    

    def _get_images(self, articles) -> List[str]:
        url_imgs = []
        for article in articles:
            img_tag = article.find('img')
            if img_tag is not None:
                src = img_tag.get('src')
                if src is not None:
                    url_imgs.append(src)
            else:
                url_imgs.append("static\\img\\no_image.jpg")
        return url_imgs
        

    def _make_categories_news(self, structure: BeautifulSoup) -> None:
        categories = structure.find_all(self.tag_to_categorize, self.class_to_categorize)

        a_tags = [category.find('a') for category in categories]
        urls: List[str] = [a_tag.get('href').strip() for a_tag in a_tags]
        categories_names: List[str] = [a_tag.text.strip() for a_tag in a_tags]

        # sol = []
        for i in range(len(urls)):
            # Fallo en esta línea por obj no iterable
            soup = BeautifulSoup(requests.get(urls[i]).text, 'lxml')
            name = categories_names[i]
            self._make_news(soup, name)
        
        # return sol


    def _build_news(self, titles: List[str], urls: List[str], imgs: List[str], category: str) -> None:
        news = []


        for i in range(len(titles)):

            # id = -1, debido a que se asignará al subirse a la BBDD
            # content = "", debido a que se asignará luego
            # journalist = -1, debido a que se han sacado de un periódico y no de un escritor autonomo/periodista
            # likes y views = 0, debido a que la noticia es nueva
            # container_id = -1, debido a que se inicializará luego
            # self, id: int, owner: str, title: str, image: str, url: str, content: str,  journalist: int, date: str, category: str, likes: int, views: int, container_id: int
            news.append(cl.News(id=-1, owner=self.owner, title=titles[i], image=imgs[i],url=urls[i],content="",journalist=-1,date=self.date,category=category,likes=0,views=0, container_id=-1))

        self.news = news


    def _make_news(self, structure: BeautifulSoup, category: str) -> None:
        if self._class:
            articles = structure.find_all(self.tag, class_=self._class)
        else:
            articles = structure.find_all(self.tag)

        urls = self._get_urls(articles)
        titles = self._get_titles(articles)
        images = self._get_images(articles)

        self._build_news(titles, urls, images, category)
    
        

