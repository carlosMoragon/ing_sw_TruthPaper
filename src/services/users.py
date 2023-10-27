# Declaraciones de los disintos tipos de usuarios
class User:
    def __init__(self, u_id: int, username: str, password: str, email: str):
        self._id = u_id
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
        return \
            (f"id: {self._id}, "
             f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}")

    def __eq__(self, other):
        return self._id == other.get_id()


class UserClient(User):

    def __init__(self, u_id: int, username: str, password: str, email: str, photo, is_checked: bool):
        super().__init__(u_id, username, password, email)
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
        return \
            (f"id: {self._id}, "
             f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}, "
             f"photo: {self._photo}, "
             f"is_checked: {self._is_checked}")


class AdministratorUser(User):
    def __init__(self,
                 u_id: int, username: str, password: str, email: str,
                 can_create: bool, can_delete: bool, can_edit: bool):
        super().__init__(u_id, username, password, email)
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
        return \
            (f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}, "
             f"can_create: {self._can_create}, "
             f"can_delete: {self._can_delete}, "
             f"can_edit: {self._can_edit}")


class CommonUser(UserClient):
    def __init__(self,
                 u_id: int, username: str, password: str, email: str, photo,
                 is_checked: bool, name: str, lastname: str, bankaccount: str):
        super().__init__(u_id, username, password, email, photo, is_checked)
        self._name = name
        self._lastname = lastname
        self._bankaccount = bankaccount

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_lastname(self, lastname):
        self._lastname = lastname

    def get_lastname(self):
        return self._lastname

    def set_banckaccount(self, bankaccount):
        self._bankaccount = bankaccount

    def get_banckaccount(self):
        return self._bankaccount

    def __str__(self):
        return \
            (f"id: {self._id}, "
             f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}, "
             f"photo: {self._photo}, "
             f"is_checked: {self._is_checked}, "
             f"name: {self._name}, "
             f"lastname: {self._lastname}, "
             f"banckaccount: {self._bankaccount}")


class CompanyUser(UserClient):
    def __init__(self,
                 u_id: int, username: str, password: str, email: str, photo,
                 is_checked: bool, company_name: str, nif: str, certification: bool):
        super().__init__(u_id, username, password, email, photo, is_checked)
        self._company_name = company_name
        self._NIF = nif
        self._certification = certification

    def set_company_name(self, company_name):
        self._company_name = company_name

    def get_company_name(self):
        return self._company_name

    def set_nif(self, nif):
        self._NIF = nif

    def get_nif(self):
        return self._NIF

    def set_certification(self, certification):
        self._certification = certification

    def get_certification(self):
        return self._certification

    def __str__(self):
        return \
            (f"id: {self._id}, "
             f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}, "
             f"photo: {self._photo}, "
             f"is_checked: {self._is_checked}, "
             f"company_name: {self._company_name}, "
             f"NIF: {self._NIF}, "
             f"certification: {self._certification}")


class Journalist(UserClient):
    def __init__(self,
                 u_id: int, username: str, password: str, email: str, photo,
                 is_checked: bool, name: str, lastname: str, certification: bool):
        super().__init__(u_id, username, password, email, photo, is_checked)
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
        return \
            (f"id: {self._id}, "
             f"username: {self._username}, "
             f"password: {self._password}, "
             f"email: {self._email}, "
             f"photo: {self._photo}, "
             f"is_checked: {self._is_checked}, "
             f"name: {self._name}, "
             f"lastname: {self._lastname}, "
             f"certification: {self._certification}")
