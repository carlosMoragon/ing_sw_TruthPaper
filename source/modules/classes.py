import re
# Declaración de clases


def validate_date(date: str) -> bool:
    # yyyy-mm-dd
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))


# Estructura de una Noticia
class News:
    def __init__(self, title, image, summary, url, comments, date, qualification: int, owner):
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

    def __str__(self):
        return f"title: {self._title}, image: {self._image}, summary: {self._summary}, url: {self._url}, comments: {self._comments}, date: {self._date}, qualification: {self._qualification}, owner: {self._owner}"


# Estructura de un comentario de una publicación
class Comment:
    def __int__(self, owner: str, text: str, date: str):
        self._owner = owner
        self._text = text
        self._date = date
        self._imgs = []

    def __init__(self, owner: str, text: str, date: str, imgs: []):
        self._owner = owner
        self._text = text
        self._date = date
        # Lista de imgs
        self._imgs = imgs

    def get_owner(self):
        return self._owner

    def set_owner(self, owner: str):
        self._owner = owner

    def set_text(self, text: str):
        self._text = text

    def get_text(self):
        return self._text

    def set_date(self, date: str):
        if validate_date(date):
            self._date = date
        else:
            print("The date hasn't been set")

    def get_date(self):
        return self._date

    def set_imgs(self, imgs: []):
        self._imgs = imgs

    def get_imgs(self):
        return self._imgs

    def add_img(self, img: str):
        self._imgs.append(img)

    # owner: str, text: str, date: str, imgs:
    def __str__(self) -> str:
        return f"owner: {self._owner}, text: {self._text}, date: {self._date}, imgs: {self._imgs}"


# Users declarations
class User:
    def __init__(self, username: str, password: str, email: str, profile_name: str, phone_number: str):
        self._username = username
        self._password = password
        self._email = email
        self._profile_name = profile_name
        self._phone_number = phone_number

    def set_username(self, username: str):
        self._username = username

    def get_username(self):
        return self._username

    def set_password(self, password: str):
        self._password = password

    def get_password(self):
        return self._password

    def set_email(self, email: str):
        self._email = email

    def get_email(self):
        return self._email

    def set_profile_name(self, profile_name):
        self._profile_name = profile_name

    def get_profile_name(self):
        return self._profile_name

    def set_phone_number(self, phone_number):
        self._phone_number = phone_number

    def get_phone_number(self):
        return self._phone_number

    # username: str, password: str, email: str, profile_name: str, phone_number: str

    def __str__(self) -> str:
        return f"username: {self._username}, password: {self._password}, email: {self._email}, profile_name: {self._profile_name}, phone_number: {self._phone_number}"


class CommonUser(User):
    def __init__(self, username: str, password: str, email: str, profile_name: str, phone_number: str, interest_themes: [], iscertificate: bool):
        super().__init__(username, password, email, profile_name, phone_number)
        self._interest_themes = interest_themes
        self._iscertificate = iscertificate

    def set_interest_themes(self, interest_themes):
        self._interest_themes = interest_themes

    def get_interest_themes(self):
        return self._interest_themes

    def set_certificate(self, iscertificate):
        self._iscertificate = iscertificate

    def get_iscertificate(self):
        return self._iscertificate

    def __str__(self) -> str:
        # interest_themes: [], iscertificate: bool
        return f"username: {self._username}, password: {self._password}, email: {self._email}, profile_name: {self._profile_name}, phone_number: {self._phone_number}, interest_themes: {self._interest_themes}, iscertificate: {self._iscertificate}"


class PremiumUser(User):
    def __init__(self, username: str, password: str, email: str, profile_name: str, phone_number: str, bank_account: str):
        super().__init__(username, password, email, profile_name, phone_number)
        self._bank_account = bank_account

    def set_bank_account(self, bank_account):
        self._bank_account = bank_account

    def get_bank_account(self):
        return self._bank_account

    def __str__(self) -> str:
        return f"username: {self._username}, password: {self._password}, email: {self._email}, profile_name: {self._profile_name}, phone_number: {self._phone_number}, banck_account{self._bank_account}"


class CompanyUser(User):
    def __init__(self, username, password, email, profile_name, phone_number, company):
        super().__init__(username, password, email, profile_name, phone_number)
        self._company = company

    def set_company(self, company):
        self._company = company

    def get_company(self):
        return self._company

    def __str__(self) -> str:
        return f"username: {self._username}, password: {self._password}, email: {self._email}, profile_name: {self._profile_name}, phone_number: {self._phone_number}, company{self._company}"
