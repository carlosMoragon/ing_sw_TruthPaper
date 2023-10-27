# Estructura de un comentario de una publicación
class Comment:

    def __init__(self, cm_id: int, likes: int, views: int, content: str, img: str, userclient_id: int):
        self._id = cm_id
        self._likes = likes
        self._views = views
        self._content = content
        self._img = img
        self._userclient_id = userclient_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, cm_id):
        self._id = cm_id

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
        return \
            (f"id: {self._id}, "
             f"likes: {self._likes}, "
             f"views: {self._views}, "
             f"content: {self._content}, "
             f"img: {self._img}, "
             f"userclient_id: {self._userclient_id}")


# Estructura de una nota en un contenido
class Note:
    def __init__(self, n_id: int, content: str, userclient_id: int):
        self._id = n_id
        self._content = content
        self._userclient_id = userclient_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, n_id):
        self._id = n_id

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


# Estructura de una noticia
class News:
    def __init__(self,
                 new_id: int, owner: str, title: str, image: str, url: str,
                 content: str, container: int, journalist: int, date: str, category: str):
        self._new_id = new_id
        self._owner = owner
        self._title = title
        self._image = image
        self._url = url
        self._content = content
        self._container = container
        self._journalist = journalist
        self._date = date
        self._category = category

    def get_category(self) -> str:
        return self._category

    def set_category(self, category):
        self._category = category

    def get_new_id(self) -> int:
        return self._new_id

    def set_new_id(self, new_id):
        self._new_id = new_id

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
        return \
            (f"id: {self._new_id}, "
             f"owner: {self._owner}, "
             f"title: {self._title}, "
             f"image: {self._image}, "
             f"url: {self._url}, "
             f"content: {self._content}, "
             f"container: {self._container}, "
             f"journalist: {self._journalist}, "
             f"date: {self._date}")

    def __eq__(self, other):
        return (
                self._new_id == other.get_id()
                and self._owner == other.get_owner()
                and self._title == other.get_title()
                and self._image == other.get_image()
                and self._url == other.get_url()
                and self._content == other.get_content()
                and self._container == other.get_container()
                and self._journalist == other.get_journalist()
                and self._date == other.get_date())

    def __hash__(self):
        return hash(self._new_id)


# Estructura de un anuncio
class Advertisement:
    def __init__(self, ad_id: int, image, content: str, url: str, views: int, companyuser_id: int):
        self._id = ad_id
        self._image = image
        self._content = content
        self._url = url
        self._views = views
        self._companyuser_id = companyuser_id

    def get_id(self) -> int:
        return self._id

    def set_id(self, ad_id):
        self._id = ad_id

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
        return \
            (f"id: {self._id}, "
             f"image: {self._image}, "
             f"content: {self._content}, "
             f"url: {self._url}, "
             f"views: {self._views}, "
             f"companyuser_id: {self._companyuser_id}")

    def __eq__(self, other):
        return self._id == other.get_id()
