# Clase de Administradores

from flask import Flask
app = Flask(__name__)

from database import DBManager as manager
# clase que crea un usuario administrador

db = manager.db


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
    return None

load_admin()




