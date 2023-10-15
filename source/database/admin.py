from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
nombre_bbdd = "truthpaper"
url_bbdd = "mysql+pymysql://root:root@localhost/" + nombre_bbdd #importar a app.py en el futuro

#utilizaremos sessions de sqlalchemy para poder hacer consultas a la base de datos
Session = sessionmaker(bind=db)
session = Session()

#Consulta de la tabla companyuser
Base = declarative_base()

class CompanyUser(Base):
    __tablename__ = 'companyuser'
    companyuser_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    nif = Column(Integer, nullable=False)
    is_company = Column(Enum('N', 'Y'))

# Crea un motor para la base de datos
engine = create_engine(url_bbdd)

# Crea una fábrica de sesiones
Session = sessionmaker(bind=engine)

# Crea una sesión
session = Session()

# Consulta la base de datos y construye los diccionarios
company_users = session.query(CompanyUser).all()

# Construye la lista de diccionarios
user_list = []
for user in company_users:
    user_dict = {
        f'companyuser{user.companyuser_id}': (user.name, user.nif, user.is_company)
    }
    user_list.append(user_dict)

print(user_list)

# Crea un diccionario con los datos de un usuario



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