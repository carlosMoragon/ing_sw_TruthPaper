#from modules import users, classes as cl
from modules import classes as cl
from typing import List, Dict
from sqlalchemy import desc
from flask import request, current_app, send_file, render_template
from PIL import Image
from io import BytesIO
import base64
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


# Hay que implementar como coger el id del usuario que se acaba de registrar --> NECESARIO HASTA QUE SE CAMBIE
user_id = 11

'''
def login(username, password) -> bool:
'''
def login(username, password): #-> bool:
    user_db =  User.query.filter_by(username=username).first()
    email_db =  User.query.filter_by(email=username).first()
    
    if user_db == None:
        user_db = email_db
    if user_db == None:
        return False
   
    if (user_db.id == 29):
        return 'admin'
    
    encoded_password = password.encode('utf-8')
    if bcrypt.check_password_hash(user_db.password, encoded_password):
        return True
    else:
        return False
    
    #return bcrypt.check_password_hash(user_db.password, password).encode('utf-8')
    # return user_db.password == password


# CONSULTA A LA BBDD PARA QUE TE COJA LAS NOTICIAS -> SE VA A LLAMAR A ESTA FUNCION DESDE APP.PY ANTES DE INICIAR
# ESTO QUE HACE AQUI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
def get_news_db(app, news, container):
    with app.app_context():
        print("entra")
        news.extend(load_news())
        container.update(ws.split_by_container(news))
        #container.update(ws.split_by_container(ws.add_new_container(news)))
'''
def save_user():
    if cl.validate_password(request.form['password']):
        if cl.validate_email(request.form['email']):
            #Si el nombre de usuario ya existe, no se puede registrar
            newUser =  User(
                username=request.form['username'],
                #password=request.form['password'],
                password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
                email=request.form['email'])

            db.session.add(newUser)
            db.session.commit()

            new_user_id = newUser.id

            newUserClient =  Userclient(
                client_id=new_user_id,
                is_checked='Y',
                photo=request.files['photo'].read()
                # photo = transform_images_to_jpeg(request.files['photo'].read())
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
        newCommonUser =  Commonuser(
            commonuser_id = new_user_id, 
            name = request.form['c_user_name'],
            lastname = request.form['c_user_lastname'],
            bankaccount = request.form['bankaccount']
        )
        db.session.add(newCommonUser)
        db.session.commit()
        return True
    
def save_companyuser(new_user_id) -> bool:
        newCompanyUser =  Companyuser(
                companyuser_id = new_user_id, 
                name = request.form['company_name'],
                bankaccount = request.form['bankaccount'],
                NIF = request.form['company_nif']
            )
        db.session.add(newCompanyUser)
        db.session.commit()
        return True

def save_journalistuser(new_user_id) -> bool:
        newJournalistUser =  Journalistuser(
                journalistuser_id = new_user_id, 
                name = request.form['journalist_name'],
                lastname = request.form['journalist_lastname'],
                certificate = request.files['certificate'].read()
            )
        db.session.add(newJournalistUser)
        db.session.commit()
        return True


#Method for admin information 
def loadUncheckedUsers():
    uncheckedUserList = []
    for user in  Userclient.query.all():
        if user.is_checked == 'N':
            usuario = User.query.filter_by(id=user.client_id).first()
            uncheckedUserList.append([usuario.username, usuario.password, usuario.email, user.client_id])
    return uncheckedUserList

# Método reescribir el estado de is_checked a 'Y'
def updateUserChecked(id):
    user =  Userclient.query.filter_by(client_id=id).first()
    user.is_checked = 'Y'
    db.session.commit()

def save_news(app, news: List[cl.News]) -> bool:
    with app.app_context():
        print("A AÑADIR NOTICIAS")
        i = last_id()
        for new in news:
            i += 1
            new_db =  New(
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
    all_comments = db.session.query( Comment).all()
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
   all_news = db.session.query( New).all()
   # all_news =  New.query.all()
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
    all_comments = db.session.query(Comment).filter_by(container_id=id).all()
    comments_objects = []
    for comment in all_comments:
        comment_obj = cl.Comment(
            id=comment.id,
            likes=comment.likes,
            views=comment.views,
            content=comment.content,
            img=comment.image,
            userclient_id=comment.userclient_id,
            container_id=comment.container_id
        )
        comments_objects.append(comment_obj)
    print("COMENTARIOS CARGADOS")
    print(comments_objects)
    return comments_objects

def is_update(fecha_actual: str) -> bool:

    print("entra en is_update")
    fecha_db = db.session.query( New.date).order_by(desc( New.date)).first()[0].strftime("%Y-%m-%d")
    print(f"{fecha_db == fecha_actual}")
    return fecha_actual == str(fecha_db)

def last_id() -> int:
    latest_new = db.session.query( New).order_by(desc( New.id)).first()
    if latest_new:
        return latest_new.id
    else:
        return 0

def transform_images_to_base64(photo_bytes):
    pil_image = Image.open(BytesIO(photo_bytes))
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    base64_image = base64.b64encode(photo_bytes).decode('utf-8')
    return base64_image

def load_image(user_id):
    user =  Userclient.query.filter_by(client_id=user_id).first()
    if user and user.photo:
        image_bytes = user.photo
        base64_image = transform_images_to_base64(image_bytes)
        return base64_image
    else:
        return None
def load_image_comment(comment_id):
    comment =  Comment.query.filter_by(id=comment_id).first()
    if comment and comment.image:
        image_bytes = comment.image
        base64_image = transform_images_to_base64(image_bytes)
        return base64_image
    else:
        return None

#Methods for containers
def load_container():
    container = cl.Container.query.all()
    container_objects = []
    for cont in container:
        container_obj = cl.Container(
            id=cont.id,
            name=cont.name
        )
        container_objects.append(container_obj)
    return container_objects

def insert_comment_container(container_id, content, userID):
    # Crea una nueva instancia de Comment
    new_comment = Comment(container_id=container_id, content=content, userclient_id=userID) # No permite subir fotos
    db.session.add(new_comment)
    db.session.commit()

def add_container(app, news: List[cl.News]):
    ids = set()
    with app.app_context():
        for new in news:
            idx = new.get_container_id()
            if idx not in ids:
                ids.add(idx)
                new_container =  Container(
                    id=idx,
                    likes=0
                )
                db.session.add(new_container)
        db.session.commit()


def get_last_container_id(app) -> int:
    with app.app_context():
        last_container = db.session.query(Container).order_by(desc(Container.id)).first()
        if last_container:
            return last_container.id
        else:
            return 0  # or any default value if no containers exist

def insert_comment(user_id, container_id, content, image_bytes):
    # Crea una nueva instancia de Comment
    new_comment = Comment(userclient_id=user_id, container_id=container_id, content=content, likes=0, views=0, image=image_bytes)
    # Agrega la nueva instancia a la sesión y guarda en la base de datos
    db.session.add(new_comment)
    db.session.commit()


def get_username(user_id):
    user =  User.query.filter_by(id=user_id).first()
    return user.username


def get_new_by_id(new_id):
    new=New.query.filter_by(id=new_id).first()
    return new

def get_comment_by_id(comment_id):
    comment=Comment.query.filter_by(id=comment_id).first()
    return comment

#Methos for pdf's
def load_pdf_certificate(user_id):
    journalistuser =  Journalistuser.query.filter_by(journalistuser_id=user_id).first()
    certificate_bytes = journalistuser.certificate 
    certificate_base64 = base64.b64encode(certificate_bytes).decode('utf-8')
    return certificate_base64


def increment_likes(new_id: int):
    noticia = New.query.filter_by(id=new_id).first()
    noticia.likes = noticia.likes + 1
    print("Like a la noticia con id: " + str(noticia.id))
    db.session.commit()


def increment_views(id_container: int):
    comentarios = Comment.query.filter_by(container_id=id_container).all()
    for comentario in comentarios:
        comentario.views += 1
        print("Vista al comentario con id: " + str(comentario.id))
    db.session.commit()


def comment_likes(comment_id: int):
    comment = Comment.query.filter_by(id=comment_id).first()
    comment.likes = comment.likes + 1
    print("Like al comentario con id: " + str(comment.id))
    db.session.commit()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Userclient(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    is_checked = db.Column(db.Enum('Y', 'N'), nullable=False)

    def __init__(self, client_id, photo, is_checked):
        self.client_id = client_id
        self.photo = photo
        self.is_checked = is_checked


class Commonuser(db.Model):
    commonuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)

    def __init__(self, commonuser_id, name, lastname, bankaccount):
        self.commonuser_id = commonuser_id
        self.name = name
        self.lastname = lastname
        self.bankaccount = bankaccount


class Companyuser(db.Model):
    companyuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    NIF = db.Column(db.Integer, nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)

    def __init__(self, companyuser_id, name, NIF, bankaccount):
        self.companyuser_id = companyuser_id
        self.name = name

        self.NIF = NIF
        self.bankaccount = bankaccount


class Journalistuser(db.Model):
    journalistuser_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    certificate = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, journalistuser_id, name, lastname, certificate):
        self.journalistuser_id = journalistuser_id
        self.name = name
        self.lastname = lastname
        self.certificate = certificate


class AdministratorUser(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    can_create = db.Column(db.Boolean, nullable=False, default=True)
    can_delete = db.Column(db.Boolean, nullable=False, default=True)
    can_edit = db.Column(db.Boolean, nullable=False, default=True)

    def _init_(self, admin_id, can_create, can_delete, can_edit):
        self.admin_id = admin_id
        self.can_create = can_create
        self.can_delete = can_delete
        self.can_edit = can_edit


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    owner = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    journalistuser_id = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    views = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id, owner, title, image, url, content, journalistuser_id, date, category, likes, views,
                 container_id):
        self.id = id
        self.owner = owner
        self.title = title
        self.image = image
        self.url = url
        self.content = content
        self.journalistuser_id = journalistuser_id
        self.date = date
        self.category = category
        self.likes = likes
        self.views = views
        self.container_id = container_id



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Integer, nullable=True, default=0)
    views = db.Column(db.Integer, nullable=True, default=0)
    content = db.Column(db.Text, nullable=True)
    image = db.Column(db.BLOB, nullable=True)
    userclient_id = db.Column(db.Integer, db.ForeignKey('userclient.client_id'), nullable=True)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'), nullable=True)

    def __init__(self, likes, views, content, image, userclient_id, container_id):
        self.likes = likes
        self.views = views
        self.content = content
        self.image = image
        self.userclient_id = userclient_id
        self.container_id = container_id


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=0)

    def __init__(self, id, likes=0):
        self.id = id
        self.likes = likes

