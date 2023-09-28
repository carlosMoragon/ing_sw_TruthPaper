from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# Implementando el webScrapping de antena3noticias
def get_news():
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
    print(url_imgs)
    print(link_news)
    print(titles)


if __name__ == '__main__':
    get_news()
    # app.run()


# Estructura de una Noticia
class News:
    def __init__(self, title, image, summary, url, comments, date, qualification, owner):
        self._title = title
        self._image = image
        self._summary = summary
        self._url = url
        self._comments = comments
        self._date = date
        self._qualification = qualification
        self._owner = owner

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_summary(self):
        return self._summary

    def set_summary(self, summary):
        self._summary = summary

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def get_comments(self):
        return self._comments

    def set_comments(self, comments):
        self._comments = comments

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._date = date

    def get_qualification(self):
        return self._qualification

    def set_qualification(self, qualification):
        self._qualification = qualification

    def get_owner(self):
        return self._owner

    def set_owner(self, owner):
        self._owner = owner


# Estructura de un comentario de una publicación
class Comment:
    def __int__(self, owner, text, date):
        self._owner = owner
        self._text = text
        self._date = date

    def __init__(self, owner, text, date, imgs):
        self._owner = owner
        self._text = text
        self._date = date
        # Lista de imgs
        self._imgs = imgs


# Users declarations
class User:
    def __init__(self, username, password, email, profile_name, phone_number):
        self.__username = username
        self.__password = password
        self.__email = email
        self.__profile_name = profile_name
        self.__phone_number = phone_number

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_profile_name(self):
        return self.__profile_name

    def get_phone_number(self):
        return self.__phone_number

    def comment(self):
        pass


class CommonUser(User):
    def __init__(self, username, password, email, profile_name, phone_number, interest_themes, certificate):
        super().__init__(username, password, email, profile_name, phone_number)
        self.__interest_themes = interest_themes
        self.__certificate = certificate

    def set_interest_themes(self, interest_themes):
        self.__interest_themes = interest_themes

    def get_interest_themes(self):
        return self.__interest_themes

    def set_certificate(self, certificate):
        self.__certificate = certificate

    def get_certificate(self):
        return self.__certificate


class PremiumUser(User):
    def __init__(self, username, password, email, profile_name, phone_number, bank_account):
        super().__init__(username, password, email, profile_name, phone_number)
        self.__bank_account = bank_account

    def set_bank_account(self, bank_account):
        self.__bank_account = bank_account

    def get_bank_account(self):
        return self.__bank_account


class CompanyUser(User):
    def __init__(self, username, password, email, profile_name, phone_number, company):
        super().__init__(username, password, email, profile_name, phone_number)
        self.__company = company

    def set_company(self, company):
        self.__company = company

    def get_company(self):
        return self.__company
