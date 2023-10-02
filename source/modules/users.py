from database import DBManager as manager

db = manager.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        

class Commonuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    
    def __init__(self, username, password, email, name, lastname):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.lastname = lastname
        

class Premiumuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    bank_account = db.Column(db.Integer, nullable=False)
    certification = db.Column(db.Boolean, nullable=False)
    
    
    def __init__(self, username, password, email, name, lastname, bank_account, certification):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.lastname = lastname
        self.bank_account = bank_account
        self.certification = certification  
        
class Journalist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    certification = db.Column(db.Boolean, nullable=False)
    
    
    def __init__(self, username, password, email, name, lastname, certification):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.lastname = lastname
        self.certification = certification  
 
class Companyuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    company_name = db.Column(db.String(50), nullable=False)
    NIF = db.Column(db.String(50), nullable=False)
    certification = db.Column(db.Boolean, nullable=False)
    
    
    def __init__(self, username, password, email, company_name, NIF, certification):
        self.username = username
        self.password = password
        self.email = email
        self.company_name = company_name
        self.NIF = NIF
        self.certification = certification  
                