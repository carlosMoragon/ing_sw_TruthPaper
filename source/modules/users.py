from database import DBManager as manager

db = manager.db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

class PremiumUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
          
class CompanyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
    