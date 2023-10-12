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

#----------PALOMA--------- (es borrable)
class AdministratorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)

    def _init_(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


lista_registros = []

# Cargar todos los usarios de la tabla "admin"
def load_admin():
    admin_data = AdministratorUser.query.all()
    for usuario in admin_data:
        lista_registros.append([usuario.username, usuario.password, usuario.email]) # Añade a la lista los datos de cada usuario
    for i, registro in enumerate(lista_registros, 1):
        print(f"Registro {i}: {registro}" )    # Imprime los datos de cada usuario
    return lista_registros





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