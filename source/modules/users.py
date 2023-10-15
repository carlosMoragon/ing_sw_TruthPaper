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
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    bank_account = db.Column(db.String(50), nullable=False)
    is_premium = db.Column(db.Boolean, nullable=False)

    
    def __init__(self, name, lastname, bank_account, is_premium):
        self.name = name
        self.lastname = lastname
        self.bank_account = bank_account
        self.is_premium = is_premium


class Companyuser(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    NIF = db.Column(db.String(50), nullable=False)
    is_company = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, name, NIF, is_company):
        self.name = name
        self.NIF = NIF
        self.is_company = is_company


# class Journalist(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.Text, nullable=True)
#     name = db.Column(db.String(50), nullable=False)
#     lastname = db.Column(db.String(50), nullable=False)
#     certification = db.Column(db.Boolean, nullable=False)
    
    
#     def __init__(self, username, password, email, name, lastname, certification):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.name = name
#         self.lastname = lastname
#         self.certification = certification    

# @app.route('/save_journalist', methods=['POST'])
# def save_J():
#     hashed_password = generate_password_hash(request.form['password'], method='sha256')
#     certification = 'certification' in request.form
#     new_user = users.journalist(request.form['username'], hashed_password, request.form['email'], request.form['name'], request.form['lastname'], certification)
#     new_G_user = users.user(request.form['username'], hashed_password, request.form['email'])
#     db.session.add(new_G_user) 
#     db.session.add(new_user) 
#     db.session.commit()
    
#     return "Saving a journalist"