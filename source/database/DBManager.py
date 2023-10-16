from flask_sqlalchemy import SQLAlchemy
from modules import users, classes as cl, web_scrapping as ws
from typing import List, Dict
db = SQLAlchemy()
from flask import request


def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
         return user_db.password == password
    else:
        return False

# CONSULTA A LA BBDD PARA QUE TE COJA LAS NOTICIAS -> SE VA A LLAMAR A ESTA FUNCION DESDE APP.PY ANTES DE INICIAR
"""
def get_news_db() -> (List[cl.News], Dict[int, List[cl.News]]):
    return None, ws.split_news(news)
"""

def save_user():
    if cl.validate_password(request.form['password']):
        if cl.validate_email(request.form['email']):
            #Si el nombre de usuario ya existe, no se puede registrar
            newUser = users.User(
                username=request.form['username'],
                password=request.form['password'],
                email=request.form['email'])

            db.session.add(newUser)
            db.session.commit()

            new_user_id = newUser.id

            newUserClient = users.Userclient(
                client_id=new_user_id,
                is_checked=True,
                photo=None
            )
            db.session.add(newUserClient)
            db.session.commit()

            return new_user_id
        else:
            print("EMAIL NO VÁLIDO")
            return -2
    else:
        print("CONTRASEÑA DÉBIL")
        return -1
    
def save_commonuser(new_user_id) -> bool:
        newCommonUser = users.Commonuser(
            commonuser_id = new_user_id, 
            name = request.form['c_user_name'],
            lastname = request.form['c_user_lastname'],
            bankaccount = request.form['bankaccount']
        )
        db.session.add(newCommonUser)
        db.session.commit()
        return True
    
def save_companyuser(new_user_id) -> bool:
        newCompanyUser = users.Companyuser(
                companyuser_id = new_user_id, 
                name = request.form['company_name'],
                bankaccount = request.form['bankaccount'],
                NIF = request.form['company_nif']
            )
        db.session.add(newCompanyUser)
        db.session.commit()
        return True

def save_journalistuser(new_user_id) -> bool:
        newJournalistUser = users.Journalistuser(
                journalistuser_id = new_user_id, 
                name = request.form['journalist_name'],
                lastname = request.form['journalist_lastname'],
                certificate = None
            )
        db.session.add(newJournalistUser)
        db.session.commit()
        return True
