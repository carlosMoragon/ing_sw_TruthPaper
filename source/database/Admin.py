# Clase de Administradores

from flask import Flask
app = Flask(__name__)

from database import DBManager as manager
from modules import users

db = manager.db
lista_admin = []
lista_admin = users.load_admin()



class Journalist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)

    def _init_(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
def journalist_name():
    journalist_data = Journalist.query.all()
    for usuario in journalist_data:
        lista_registros.append([usuario.username, usuario.password, usuario.email])
    for i, registro in enumerate(lista_registros, 1):
        print(f"Registro {i}: {registro}" )
    return None




