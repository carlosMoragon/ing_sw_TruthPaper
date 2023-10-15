from database import DBManager as manager
db = manager.db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=True)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Userclient(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    is_checked = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, client_id, photo, is_checked):
        self.client_id = client_id
        self.photo = photo
        self.is_checked = is_checked   
        
class Commonuser(db.Model):
    commonuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)
    
    def __init__(self, commonuser_id, name, lastname, bankaccount):
        self.commonuser_id = commonuser_id
        self.name = name
        self.lastname = lastname
        self.bankaccount = bankaccount

class Companyuser(db.Model):
    companyuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    NIF = db.Column(db.Integer, nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)
    
    def __init__(self, companyuser_id, name, NIF, bankaccount):
        self.companyuser_id = companyuser_id
        self.name = name
        self.NIF = NIF
        self.bankaccount = bankaccount

class Journalistuser(db.Model):
    journalistuser_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    certificate = db.Column(db.LargeBinary, nullable=True)
    
    def __init__(self, journalistuser_id, name, lastname, certificate):
        self.journalistuser_id = journalistuser_id
        self.name = name
        self.lastname = lastname
        self.certificate = certificate    
