from database import DBManager as manager

db = manager.db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    profilephoto = db.Column(db.Binary, nullable=True)
    
    def __init__(self, username, password, email, profilephoto):
        self.username = username
        self.password = password
        self.email = email
        self.profilephoto = profilephoto

class Commonuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.Binary, nullable=True)
    
    def __init__(self, username, password, email, name, lastname, photo):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.lastname = lastname
        self.photo = photo


class Companyuser(db.Model):

    def __init__(self, username, password, email, company_name, NIF):
        self.username = username
        self.password = password
        self.email = email
        self.company_name = company_name
        self.NIF = NIF
        # self.certification = certification

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    company_name = db.Column(db.String(50), nullable=False)
    NIF = db.Column(db.String(50), nullable=False)
    # certification = db.Column(db.Boolean, nullable=False)

 
# class AdministratorUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.Text, nullable=True)
    
#     def __init__(self, username, password, email):
#         self.username = username
#         self.password = password
#         self.email = email
  

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