from modules import users, classes as cl, web_scrapping as ws
from typing import List, Dict
from sqlalchemy import desc
from flask import request, current_app, send_file, render_template
from PIL import Image
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Hay que implementar como coger el id del usuario que se acaba de registrar
user_id = 11

def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    email_db = users.User.query.filter_by(email=username).first()
    
    if user_db == None:
        user_db = email_db
    return user_db.password == password


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
                #password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
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
                certificate = request.files['certificate'].read()
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
            img=comment.image,
            userclient_id=comment.userclient_id,
            container_id=comment.container_id
        )
        comments_objects.append(comment_obj)
    print("COMENTARIOS CARGADOS")
    print(comments_objects)
    return comments_objects

def is_update(fecha_actual: str) -> bool:
    # print(db.session.query(users.New.date).order_by(desc(users.New.date)).first())
    
    return fecha_actual == db.session.query(users.New.date).order_by(desc(users.New.date)).first()



def is_update(fecha_actual: str) -> bool:
    return False

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
'''
def add_container(app, news: List[cl.News]):
    with app.app_context():
        for news_item in news:
            container_id = set(news_item.get_container_id())  # Call the method to get the integer value
            new_container = users.Container(
                id=container_id,
                likes=0
            )
            db.session.add(new_container)
        db.session.commit()

'''
def add_container(app, news: List[cl.News]):
    ids = set()
    with app.app_context():
        for new in news:
            idx = new.get_container_id()
            if idx not in ids:
                ids.add(idx)
                new_container = users.Container(
                    id=idx,
                    likes=0
                )
                db.session.add(new_container)
        db.session.commit()


def get_last_container_id():
    return db.session.query(users.Container).order_by(desc(users.Container.id)).first()

def insert_comment(user_id, container_id, content):
    # Crea una nueva instancia de Comment
    new_comment = users.Comment(user_id=user_id, container_id=container_id, content=content)

    # Agrega la nueva instancia a la sesión y guarda en la base de datos
    db.session.add(new_comment)
    db.session.commit()


def get_username(user_id):
    user = users.User.query.filter_by(id=user_id).first()
    return user.username

# def render_pdf(user_id):
#     pdf_bytes = load_pdf_certificate(user_id)

#     pdf_document = fitz.open(BytesIO(pdf_bytes))
#     images_base64 = []

#     #for page_num in range(pdf_document.page_count):
#             # page = pdf_document[page_num]
#     page = pdf_document[0]
#     image = page.get_pixmap()
#     image_data = image.get_image_data()
#     image_base64 = base64.b64encode(image_data).decode('utf-8')
#     images_base64.append(image_base64)

#     return send_file(images_base64, mimetype='image/jpeg')
#     #return images_base64
    
# def load_pdf_certificate(user_id):
#     journalistuser = users.Journalistuser.query.filter_by(journalistuser_id=user_id).first()
#     # print(journalistuser)
#     if journalistuser and journalistuser.certificate: 
#         certificate = journalistuser.certificate 
#         # documento = Image.open(BytesIO(certificate))
#         # print(type(documento))
#         return convert_pdf_to_images(certificate)
#     else:
#         return None
    

# def convert_pdf_to_images(pdf_data):
#     try:
#         # Usa io.BytesIO en lugar de fitz.BytesIO
#         pdf_stream = io.BytesIO(pdf_data)
#         pdf_document = fitz.open(pdf_stream)
#         images = []
        
#         for page_number in range(pdf_document.page_count):
#             page = pdf_document[page_number]
#             # Convierte la página en imagen RGBA (formato compatible con PIL)
#             image_data = page.get_pixmap()
#             img = Image.frombytes("RGB", [image_data.width, image_data.height], image_data.samples)
#             # Agrega la imagen a la lista de imágenes
#             images.append(img)
        
#         return images
#     except Exception as e:
#         print(f"Error al procesar el PDF: {e}")
#         return None
