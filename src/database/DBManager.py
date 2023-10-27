from flask import request
from flask_sqlalchemy import SQLAlchemy
from typing import List
from src.models import model_users, model_news
from src.services import contents as cntnt, web_scraping as ws
from src.utils import validations as vld


db = SQLAlchemy()


def login(username, password) -> bool:
    user_db = model_users.User.query.filter_by(username=username).first()
    if user_db:
        return user_db.password == password
    else:
        return False


def get_news_db(news, container):
    news.extend(load_new())
    container.update(ws.split_news(news))  # Aún no existe el método


def save_user():
    if vld.validate_password(request.form['password']):
        if vld.validate_email(request.form['email']):
            # Si el nombre de usuario ya existe, no se puede registrar
            new_user = model_users.User(
                username=request.form['username'],
                password=request.form['password'],
                email=request.form['email'])

            db.session.add(new_user)
            db.session.commit()

            new_user_id = new_user.id

            new_user_client = model_users.UserClient(
                client_id=new_user_id,
                is_checked=True,
                photo=None
            )
            db.session.add(new_user_client)
            db.session.commit()

            return new_user_id
        else:
            print("EMAIL NO VÁLIDO")
            return -2
    else:
        print("CONTRASEÑA DÉBIL")
        return -1


def save_common_user(new_user_id) -> bool:
    new_common_user = model_users.CommonUser(
        commonuser_id=new_user_id,
        name=request.form['c_user_name'],
        lastname=request.form['c_user_lastname'],
        bankaccount=request.form['bankaccount']
    )
    db.session.add(new_common_user)
    db.session.commit()
    return True


def save_company_user(new_user_id) -> bool:
    new_company_user = model_users.CompanyUser(
        companyuser_id=new_user_id,
        name=request.form['company_name'],
        nif=request.form['company_nif'],
        bankaccount=request.form['bankaccount']
    )
    db.session.add(new_company_user)
    db.session.commit()
    return True


def save_journalist_user(new_user_id) -> bool:
    new_journalist_user = model_users.JournalistUser(
        journalistuser_id=new_user_id,
        name=request.form['journalist_name'],
        lastname=request.form['journalist_lastname'],
        certificate=None
    )
    db.session.add(new_journalist_user)
    db.session.commit()
    return True


# Method for admin information
def load_unchecked_users():
    unchecked_user_list = []
    for user in model_users.UserClient.query.all():
        if user.is_checked == 'N':
            usuario = model_users.User.query.filter_by(id=user.client_id).first()
            unchecked_user_list.append([usuario.username, usuario.password, usuario.email])
    return unchecked_user_list


# Método reescribir el estado de is_checked a 'Y'
def update_user_checked(user_id):
    user = model_users.User.query.filter_by(id=user_id).first()
    if user:
        user.is_checked = 'Y'
        db.session.commit()


def save_news(news: List[cntnt.News]) -> bool:
    for new in news:
        new_db = model_news.New(
            new_id=new.get_new_id(),
            owner=new.get_owner(),
            title=new.get_title(),
            image=new.get_image(),
            url=new.get_url(),
            content=new.get_content(),
            container=new.get_container(),
            journalistuser_id=new.get_journalist(),
            date=new.get_date(),
            category=new.get_category()
        )
        db.session.add(new_db)
    db.session.commit()
    return True


def load_new() -> List[cntnt.News]:
    all_news = db.session.query(model_news.New).all()
    # all_news = users.New.query.all()
    news_objects = []
    for news in all_news:
        news_obj = cntnt.News(
            new_id=news.new_id,
            owner=news.owner,
            title=news.title,
            image=news.image,
            url=news.url,
            content=news.content,
            container=news.container,
            journalist=news.journalistuser_id,
            date=news.date.strftime('%Y-%m-%d'),
            category=news.category
        )
        news_objects.append(news_obj)
    return news_objects


def get_dbmanager():
    return db
