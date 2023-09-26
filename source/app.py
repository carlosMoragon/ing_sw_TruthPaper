from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


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
