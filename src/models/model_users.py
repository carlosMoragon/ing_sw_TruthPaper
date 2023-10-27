from flask_sqlalchemy import SQLAlchemy


class User(SQLAlchemy().Model):
    id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, unique=True, autoincrement=True)
    username = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)
    password = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)
    email = SQLAlchemy().Column(SQLAlchemy().Text, nullable=True)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class UserClient(SQLAlchemy().Model):
    client_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, autoincrement=True)
    photo = SQLAlchemy().Column(SQLAlchemy().LargeBinary, nullable=True)
    is_checked = SQLAlchemy().Column(SQLAlchemy().Enum('Y', 'N'), nullable=False)
    
    def __init__(self, client_id, photo, is_checked):
        self.client_id = client_id
        self.photo = photo
        self.is_checked = is_checked   


class CommonUser(SQLAlchemy().Model):
    commonuser_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, autoincrement=True)
    name = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)
    lastname = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)
    bankaccount = SQLAlchemy().Column(SQLAlchemy().String(70), nullable=False)
    
    def __init__(self, commonuser_id, name, lastname, bankaccount):
        self.commonuser_id = commonuser_id
        self.name = name
        self.lastname = lastname
        self.bankaccount = bankaccount


class CompanyUser(SQLAlchemy().Model):
    companyuser_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, autoincrement=True)
    name = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)
    nif = SQLAlchemy().Column(SQLAlchemy().Integer, nullable=False)
    bankaccount = SQLAlchemy().Column(SQLAlchemy().String(70), nullable=False)
    
    def __init__(self, companyuser_id, name, nif, bankaccount):
        self.companyuser_id = companyuser_id
        self.name = name
        self.NIF = nif
        self.bankaccount = bankaccount


class JournalistUser(SQLAlchemy().Model):
    journalistuser_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, unique=True, autoincrement=True)
    name = SQLAlchemy().Column(SQLAlchemy().String(50), nullable=False)
    lastname = SQLAlchemy().Column(SQLAlchemy().String(50), nullable=False)
    certificate = SQLAlchemy().Column(SQLAlchemy().LargeBinary, nullable=True)
    
    def __init__(self, journalistuser_id, name, lastname, certificate):
        self.journalistuser_id = journalistuser_id
        self.name = name
        self.lastname = lastname
        self.certificate = certificate    


class AdministratorUser(SQLAlchemy().Model):
    admin_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, unique=True, autoincrement=True)
    can_create = SQLAlchemy().Column(SQLAlchemy().Boolean, nullable=False, default=True)
    can_delete = SQLAlchemy().Column(SQLAlchemy().Boolean, nullable=False, default=True)
    can_edit = SQLAlchemy().Column(SQLAlchemy().Boolean, nullable=False, default=True)

    def _init_(self, admin_id, can_create, can_delete, can_edit):
        self.admin_id = admin_id
        self.can_create = can_create
        self.can_delete = can_delete    
        self.can_edit = can_edit    
