from flask_sqlalchemy import SQLAlchemy
from modules import users, classes as cl, web_scrapping as ws
from typing import List, Dict
from sqlalchemy import desc
from flask import request, current_app, send_file
from PIL import Image
from io import BytesIO
db = SQLAlchemy()

def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
         return user_db.password == password
    else:
        return False

# CONSULTA A LA BBDD PARA QUE TE COJA LAS NOTICIAS -> SE VA A LLAMAR A ESTA FUNCION DESDE APP.PY ANTES DE INICIAR


def get_news_db(app, news, container):
    with app.app_context():
        print("entra")
        news.extend(load_news())
        container.update(ws.split_by_container(news))
        #container.update(ws.split_by_container(ws.add_new_container(news)))

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
                is_checked='Y',
                photo=request.files['photo'].read()
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
    user = users.Userclient.query.filter_by(client_id=id).first()
    print(user.is_checked)
    user.is_checked = 'Y'
    db.session.commit()

def save_news(app, news: List[cl.News]) -> bool:
    with app.app_context():
        i = last_id()
        for new in news:
            i += 1
            new_db = users.New(
                id=i,
                owner=new.get_owner(),
                title=new.get_title(),
                image=new.get_image(),
                url=new.get_url(),
                content=new.get_content(),
                container_id=new.get_container_id(),# Se supone que guarda el id de contenedor en la columna correcta
                journalistuser_id=31,
                date=new.get_date(),
                category=new.get_category(),
                likes=new.get_likes(),
                views=new.get_views()

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
   # all_news = users.New.query.all()
   news_objects = []
   for news in all_news:
       news_obj = cl.News(
           id=news.id,
           owner=news.owner,
           title=news.title,
           image=news.image,
           url=news.url,
           content=news.content,
           container_id=news.container_id,
           journalist=news.journalistuser_id,
           date=news.date.strftime('%Y-%m-%d'),
           category=news.category,
           likes=news.likes,
           views=news.views
       )
       news_objects.append(news_obj)

   return news_objects

def load_comments(id: int) -> List[cl.Comment]:
    all_comments = db.session.query(users.Comment).filter_by(container_id=id).all()
    comments_objects = []
    for comment in all_comments:
        comment_obj = cl.Comment(
            id=comment.id,
            likes=comment.likes,
            views=comment.views,
            content=comment.content,
            img=comment.img,
            userclient_id=comment.userclient_id,
            container_id=comment.container_id
        )
        comments_objects.append(comment_obj)
    print("COMENTARIOS CARGADOS")
    print(comments_objects)
    return comments_objects


''' Método para actualizar columna, BORRAR 
def update_container_for_news(news_list):
    existing_containers = set()
    for news in news_list:
        container_id = news.get_container()
        existing_containers.add(container_id)

    for container_id in existing_containers:
        container = users.Container.query.filter_by(id=container_id).first()

        if container is None:
            new_container = users.Container(id=container_id, likes=0)
            db.session.add(new_container)

    db.session.commit()
    '''
'''
def is_update(fecha_actual: str) -> bool:
    # print(db.session.query(users.New.date).order_by(desc(users.New.date)).first())
    
    return fecha_actual == db.session.query(users.New.date).order_by(desc(users.New.date)).first()
'''


def is_update(fecha_actual: str) -> bool:
    print("entra en is_update")
    fecha_db = db.session.query(users.New.date).order_by(desc(users.New.date)).first()[0].strftime("%Y-%m-%d")
    print(f"{fecha_db == fecha_actual}")
    return fecha_actual == str(fecha_db)

'''
def last_id() -> int:
    return db.session.query(users.New).order_by(desc(users.New.id)).first()
'''


def last_id() -> int:
    latest_new = db.session.query(users.New).order_by(desc(users.New.id)).first()
    if latest_new:
        return latest_new.id
    else:
        return 0


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
    
def load_image(user_id):
    user = users.Userclient.query.filter_by(client_id=user_id).first()
    if user and user.photo:
        image_bytes = user.photo
        image = Image.open(BytesIO(image_bytes))
        return image
    else:
        return None