from flask import Flask
from database import DBManager as manager
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = manager.db

# Definir el modelo
Base = declarative_base()

lista_registros = []

# Cargar todos los usarios de la tabla "admin"
'''
def load_admin():
    admin_data = AdministratorUser.query.all()

    for usuario in admin_data:
        lista_registros.append([usuario.username, usuario.password, usuario.email]) # Añade a la lista los datos de cada usuario

    for i, registro in enumerate(lista_registros, 1):
            print(f"Registro {i}: {registro}" )    # COMPROBACIÓN
    return lista_registros
'''