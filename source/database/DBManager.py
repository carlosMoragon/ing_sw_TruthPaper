from flask_sqlalchemy import SQLAlchemy
from modules import users, classes as cl, web_scrapping as ws
from typing import List, Dict
db = SQLAlchemy()
from sqlalchemy import desc
from flask import request, current_app


def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
         return user_db.password == password
    else:
        return False

# CONSULTA A LA BBDD PARA QUE TE COJA LAS NOTICIAS -> SE VA A LLAMAR A ESTA FUNCION DESDE APP.PY ANTES DE INICIAR


#def get_news_db(news, container):
#    news.extend(load_new())
#    container.update(ws.split_news(news))

def get_news_db(app, news, container):
    with app.app_context():
        print("entra")
        news.extend(load_news())
        container.update(ws.split_by_container(news))

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
            uncheckedUserList.append([usuario.username, usuario.password, usuario.email, user.client_id])
    return uncheckedUserList

# Método reescribir el estado de is_checked a 'Y'
def updateUserChecked(id):
    print("entra en la funcion")
    user = users.Userclient.query.filter_by(client_id=id).first()
    print("==================")
    print(user.is_checked)
    print("==================")
    user.is_checked = 'Y'
    db.session.commit()

#def save_news(news: List[cl.News]) -> bool:
#   for new in news:
#       new_db = users.New(
#           owner=new.get_owner(),
#           title=new.get_title(),
#           image=new.get_image(),
#           url=new.get_url(),
#           content=new.get_content(),
#           container=new.get_container(),
#           journalistuser_id=new.get_journalist(),
#           date=new.get_date(),
#           category=new.get_category()
#       )
#       db.session.add(new_db)
#       print("b")
#   db.session.commit()
#   return True


def save_news(app, news: List[cl.News]) -> bool:
    with app.app_context():
        i = last_id()
        for new in news:
            i +=1
            new_db = users.New(
                id=i,
                owner=new.get_owner(),
                title=new.get_title(),
                image=new.get_image(),
                url=new.get_url(),
                content=new.get_content(),
                container=new.get_container(),
                journalistuser_id=31,
                date=new.get_date(),
                category=new.get_category(),
                likes= new.get_likes(),
                views = new.get_views(),

            )
            db.session.add(new_db)

        db.session.commit()
        return True

def load_comments()-> List[cl.Comment]:
    all_comments = db.session.query(users.Comment).all()
    comments_objects = []
    for comment in all_comments:
        comment_obj = cl.Comment(
            id=comment.id,
            img=comment.img,
            userclient_id=comment.userclient_id,
        )
        comments_objects.append(comment_obj)

    return comments_objects


def load_news() -> List[cl.News]:
   all_news = db.session.query(users.New).all()
   #all_news = users.New.query.all()
   news_objects = []
   for news in all_news:
       news_obj = cl.News(
           id=news.id,
           owner=news.owner,
           title=news.title,
           image=news.image,
           url=news.url,
           content=news.content,
           container=news.container,
           journalist=news.journalistuser_id,
           date=news.date.strftime('%Y-%m-%d'),
           category=news.category,
           likes=news.likes,
           views=news.views
       )
       news_objects.append(news_obj)

   return news_objects


def is_update(fecha_actual: str) -> bool:
    return fecha_actual == db.session.query(users.New.date).order_by(desc(users.New.date)).first()


def last_id() -> int:
    return db.session.query(users.New).order_by(desc(users.New.id)).first()
