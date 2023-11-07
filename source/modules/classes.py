import re
from typing import List
# from modules import web_scrapping as ws
# Declaración de clases


def validate_date(date: str) -> bool:
    # yyyy-mm-dd
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date))


def validate_password(password: str) -> bool:
    # Busca que tenga al menos 4 numeros, 1 mayuscula, 1 caracter especial y 8 digitos
    return bool(re.match(r'^(?=.*\d{4,})(?=.*[A-Z])(?=.*[\W_]).{8,}$', password))


def validate_email(email: str) -> bool:
    # Busca una expresión del tipo (string1)@(string2).(2+characters)
    return bool(re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))


# Estructura de un comentario de una publicación
class Comment:

    def __init__(self, id: int, likes: int, views: int, content: str, img: str, userclient_id: int):
        self._id = id
        self._likes = likes
        self._views = views
        self._content = content
        self._img = img
        self._userclient_id = userclient_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, id):
        self._id = id

    def get_likes(self) -> int:
        return self._likes

    def set_likes(self, likes):
        self._likes = likes

    def get_views(self) -> int:
        return self._views

    def set_views(self, views):
        self._views = views

    def get_content(self) -> str:
        return self._content

    def set_content(self, content):
        self._content = content

    def get_img(self) -> str:
        return self._img

    def set_img(self, img):
        self._img = img

    def get_userclient_id(self) -> int:
        return self._userclient_id

    def set_userclient_id(self, userclient_id):
        self._userclient_id = userclient_id

    def __str__(self) -> str:
        return f"id: {self._id}, likes: {self._likes}, views: {self._views}, content: {self._content}, img: {self._img}, userclient_id: {self._userclient_id}"


# Users declarations
class User:
    def __init__(self, id: int, username: str, password: str, email: str):
        self._id = id
        self._username = username
        self._password = password
        self._email = email

    def set_username(self, username: str):
        self._username = username

    def get_username(self) -> str:
        return self._username

    def set_password(self, password: str):
        self._password = password

    def get_password(self) -> str:
        return self._password

    def set_email(self, email: str):
        self._email = email

    def get_email(self) -> str:
        return self._email

    def __str__(self) -> str:
        return f"id: {self._id}, username: {self._username}, password: {self._password}, email: {self._email}"

    def __eq__(self, other):
        return self._id == other.get_id()


class UserClient(User):

    def __init__(self, id: int, username: str, password: str, email: str, photo, is_checked: bool):
        super().__init__(id, username, password, email)
        self._photo = photo
        self._is_checked = is_checked

    def set_photo(self, photo):
        self._photo = photo

    def get_photo(self):
        return self._photo

    def set_is_checked(self, is_checked):
        self._is_checked = is_checked

    def get_is_checked(self):
        return self._is_checked

    def __str__(self):
        return f"id: {self._id}, username: {self._username}, password: {self._password}, email: {self._email}, photo: {self._photo}, is_checked: {self._is_checked}"


class AdministratorUser(User):
    def __init__(self, username: str, password: str, email: str, can_create: bool, can_delete: bool, can_edit: bool):
        super().__init__(username, password, email)
        self._can_create = can_create
        self._can_delete = can_delete
        self._can_edit = can_edit

    def get_can_create(self):
        return self._can_create

    def get_can_delete(self):
        return self._can_delete

    def get_can_edit(self):
        return self._can_edit

    def __str__(self):
        return f"username: {self._username}, password: {self._password}, email: {self._email}, can_create: {self._can_create}, can_delete: {self._can_delete}, can_edit: {self._can_edit}"


class CommonUser(UserClient):
    def __init__(self, id: int, username: str, password: str, email: str, photo, is_checked: bool, name: str, lastname: str, banckaccount: str):
        super().__init__(id, username, password, email, photo, is_checked)
        self._name = name
        self._lastname = lastname
        self._banckaccount = banckaccount

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_lastname(self, lastname):
        self._lastname = lastname

    def get_lastname(self):
        return self._lastname

    def set_banckaccount(self, banckaccount):
        self._banckaccount = banckaccount

    def get_banckaccount(self):
        return self._banckaccount

    def __str__(self):
        return f"id: {self._id}, username: {self._username}, password: {self._password}, email: {self._email}, photo: {self._photo}, is_checked: {self._is_checked}, name: {self._name}, lastname: {self._lastname}, banckaccount: {self._banckaccount}"


class CompanyUser(UserClient):
    def __init__(self, id: int, username: str, password: str, email: str, photo, is_checked: bool, company_name: str, NIF: str, certification: bool):
        super().__init__(id, username, password, email, photo, is_checked)
        self._company_name = company_name
        self._NIF = NIF
        self._certification = certification

    def set_company_name(self, company_name):
        self._company_name = company_name

    def get_company_name(self):
        return self._company_name

    def set_NIF(self, NIF):
        self._NIF = NIF

    def get_NIF(self):
        return self._NIF

    def set_certification(self, certification):
        self._certification = certification

    def get_certification(self):
        return self._certification

    def __str__(self):
        return f"id: {self._id}, username: {self._username}, password: {self._password}, email: {self._email}, photo: {self._photo}, is_checked: {self._is_checked}, company_name: {self._company_name}, NIF: {self._NIF}, certification: {self._certification}"

class Journalist(UserClient):
    def __init__(self,id: int, username: str, password: str, email: str, photo, is_checked: bool, name: str, lastname: str, certification: bool):
        super().__init__(id, username, password, email, photo, is_checked)
        self._name = name
        self._lastname = lastname
        self._certification = certification

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_lastname(self, lastname):
        self._lastname = lastname

    def get_lastname(self):
        return self._lastname

    def set_certification(self, certification):
        self._certification = certification

    def get_certification(self):
        return self._certification

    def __str__(self):
        return f"id: {self._id}, username: {self._username}, password: {self._password}, email: {self._email}, photo: {self._photo}, is_checked: {self._is_checked}, name: {self._name}, lastname: {self._lastname}, certification: {self._certification}"


class advertisement:
    def __init__(self, id: int, image, content: str, url: str, views: int, companyuser_id: int):
        self._id = id
        self._image = image
        self._content = content
        self._url = url
        self._views = views
        self._companyuser_id = companyuser_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, id):
        self._id = id

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_content(self) -> str:
        return self._content

    def set_content(self, content):
        self._content = content

    def get_url(self) -> str:
        return self._url

    def set_url(self, url):
        self._url = url

    def get_views(self) -> int:
        return self._views

    def set_views(self, views):
        self._views = views

    def get_companyuser_id(self) -> int:
        return self._companyuser_id

    def set_companyuser_id(self, companyuser_id):
        self._companyuser_id = companyuser_id

    def __str__(self) -> str:
        return f"id: {self._id}, image: {self._image}, content: {self._content}, url: {self._url}, views: {self._views}, companyuser_id: {self._companyuser_id}"

    def __eq__(self, other):
        return self._id == other.get_id()


class Note:
    def __init__(self, id: int, content: str, userclient_id: int):
        self._id = id
        self._content = content
        self._userclient_id = userclient_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, id):
        self._id = id

    def get_content(self) -> str:
        return self._content

    def set_content(self, content):
        self._content = content

    def get_userclient_id(self) -> int:
        return self._userclient_id

    def set_userclient_id(self, userclient_id):
        self._userclient_id = userclient_id

    def __str__(self) -> str:
        return f"id: {self._id}, content: {self._content}, userclient_id: {self._userclient_id}"

    def __eq__(self, other):
        return self._id == other.get_id()


# Estructura de una Noticia
class News:
    def __init__(self, id: int, owner: str, title: str, image: str, url: str, content: str, container: int, journalist: int, date: str, category: str):
        self._id = id
        self._owner = owner
        self._title = title
        self._image = image
        self._url = url
        self._content = content
        self._container = container
        self._journalist = journalist
        self._date = date
        self._category = category

    # Getters y Setters
    def get_category(self) -> str:
        return self._category

    def set_category(self, category):
        self._category = category

    def get_id(self) -> int:
        return self._id

    def set_id(self, id):
        self._id = id

    def get_owner(self) -> str:
        return self._owner

    def set_owner(self, owner):
        self._owner = owner

    def get_title(self) -> str:
        return self._title

    def set_title(self, title):
        self._title = title

    def get_image(self) -> str:
        return self._image

    def set_image(self, image):
        self._image = image

    def get_url(self) -> str:
        return self._url

    def set_url(self, url):
        self._url = url

    def get_content(self) -> str:
        return self._content

    def set_content(self, content):
        self._content = content

    def get_container(self) -> int:
        return self._container

    def set_container(self, container):
        self._container = container

    def get_journalist(self) -> int:
        return self._journalist

    def set_journalist(self, journalist):
        self._journalist = journalist

    def get_date(self) -> str:
        return self._date

    def set_date(self, date):
        self._date = date

    def __str__(self) -> str:
        return f"id: {self._id}, owner: {self._owner}, title: {self._title}, image: {self._image}, url: {self._url}, content: {self._content}, container: {self._container}, journalist: {self._journalist}, date: {self._date}"

    def __eq__(self, other):
        return self._id == other.get_id() and self._owner == other.get_owner() and self._title == other.get_title() and self._image == other.get_image() and self._url == other.get_url() and self._content == other.get_content() and self._container == other.get_container() and self._journalist == other.get_journalist() and self._date == other.get_date()

    def __hash__(self):
        return hash(self._id)
    
    class Container:
        def __init__(self, id: int, likes: str):
            self._id = id
            self._likes = likes

        def get_id(self) -> int:
            return self._id

        def set_id(self, id):
            self._id = id

        def get_likes(self) -> str:
            return self._likes

        def set_likes(self, likes):
            self._likes = likes
