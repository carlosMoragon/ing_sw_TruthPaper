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


def get_news_db(news, container):
    news.extend(load_new())
    container.update(ws.split_news(news))


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


#Method for admin information 
def loadUncheckedUsers():
    uncheckedUserList = []
    for user in users.Userclient.query.all():
        if user.is_checked == 'N':
            usuario = users.User.query.filter_by(id=user.client_id).first()
            uncheckedUserList.append([usuario.username, usuario.password, usuario.email])
    return uncheckedUserList

#Método reescribir el estado de is_checked a 'Y'
def updateUserChecked(user_id):
    user = users.User.query.filter_by(id=user_id).first()
    if user:
        user.is_checked = 'Y'
        db.session.commit()

#MORAGON TENGO QUE PROBAR ESTO AUN
def save_new(owner, title, image, url, content, container, journalistuser_id, date, category):
    new = users.New(owner=owner, title=title, image=image, url=url, content=content, container=container, journalistuser_id=journalistuser_id, date=date, category=category)
    db.session.add(new)
    db.session.commit()
    return True

# def save_news(news: List[cl.News]) -> bool:
#    for new in news:
#        new_db = users.New(
#            owner=new.get_owner(),
#            title=new.get_title(),
#            image=new.get_image(),
#            url=new.get_url(),
#            content=new.get_content(),
#            container=new.get_container(),
#            journalistuser_id=new.get_journalist(),
#            date=new.get_date(),
#            category=new.get_category()
#        )
#        db.session.add(new_db)
#    db.session.commit()
#    return True

    
def load_new():
    news = []
    article = users.New.query.limit(30).all()
    for i in article:
        news.append(i)
    return news

# def load_new() -> List[cl.News]:
#    all_news = db.session.query(users.New).all()
#    news_objects = []
#    for news in all_news:
#        news_obj = cl.News(
#            id=news.id,
#            owner=news.owner,
#            title=news.title,
#            image=news.image,
#            url=news.url,
#           content=news.content,
#            container=news.container,
#            journalist=news.journalistuser_id,
#            date=news.date.strftime('%Y-%m-%d'),
#            category=news.category
#        )
#        news_objects.append(news_obj)
#    return news_objects
