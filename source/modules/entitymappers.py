from database.DBManager import db
from modules import classes as cl
from typing import List, Dict
from sqlalchemy import desc
from io import BytesIO
from PIL import Image
import base64


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    owner = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    journalistuser_id = db.Column(db.Integer, db.ForeignKey('journalistuser.journalistuser_id'))#db.Column(db.Integer)
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

    def save_news(app, news: List[cl.News]) -> bool:
        with app.app_context():
            print("A AÑADIR NOTICIAS")
            i = last_id()
            for new in news:
                # container_id = new.get_container_id()
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

    
    def load_news() -> List[cl.News]:
        all_news = db.session.query(New).all()
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
    
    def get_new_by_id(new_id):
        new=New.query.filter_by(id=new_id).first()
        return new

    def increment_likes(new_id: int):
        noticia = New.query.filter_by(id=new_id).first()
        noticia.likes = noticia.likes + 1
        #print("Like a la noticia con id: " + str(noticia.id))
        db.session.commit()


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=0)

    def __init__(self, id, likes=0):
        self.id = id
        self.likes = likes
    
    def get_last_container_id(app) -> int:
        with app.app_context():
            last_container = db.session.query(Container).order_by(desc(Container.id)).first()
            if last_container:
                return last_container.id
            else:
                return 0  # or any default value if no containers exist
            
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
    
    #Sabra dios cual de los dos se usa y cual no
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
    
    def comment_likes(comment_id: int):
        comment = Comment.query.filter_by(id=comment_id).first()
        comment.likes = comment.likes + 1
        print("Like al comentario con id: " + str(comment.id))
        db.session.commit()
    
    def increment_views(id_container: int):
        comentarios = Comment.query.filter_by(container_id=id_container).all()
        for comentario in comentarios:
            comentario.views += 1
            print("Vista al comentario con id: " + str(comentario.id))
        db.session.commit()
    
    def get_comment_by_id(comment_id):
        comment=Comment.query.filter_by(id=comment_id).first()
        return comment
    
    def insert_comment(user_id, container_id, content, image_bytes):
        # Crea una nueva instancia de Comment
        new_comment = Comment(userclient_id=user_id, container_id=container_id, content=content, likes=0, views=0, image=image_bytes)
        # Agrega la nueva instancia a la sesión y guarda en la base de datos
        db.session.add(new_comment)
        db.session.commit()
        
    def insert_comment_container(container_id, content, userID):
        # Crea una nueva instancia de Comment
        new_comment = Comment(container_id=container_id, content=content, userclient_id=userID) # No permite subir fotos
        db.session.add(new_comment)
        db.session.commit()
        
    def load_image_comment(comment_id):
        comment =  Comment.query.filter_by(id=comment_id).first()
        if comment and comment.image:
            image_bytes = comment.image
            base64_image = transform_images_to_base64(image_bytes)
            return base64_image
        else:
            return None
        
    
class UserSavedNews(db.Model):    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iduser = db.Column(db.Integer, nullable=True, default=0)
    idnews= db.Column(db.Integer, nullable=True, default=0)
    
    def __init__(self, id, iduser, idnews):
        self.id = id
        self.iduser = iduser
        self.idnews = idnews
    
    def load_ids_news_saved_by_user(id_user):
        id_news_saved_by_user = db.session.query(UserSavedNews.idnews).filter_by(iduser=id_user).all()
        return id_news_saved_by_user   #Esto solo devuelves los ids de las noticias guardadas por el usuario (hay que ligarlo con los metodos de cargar noticias)
    
    def user_saves_new(id_user, id_new):
        new_user_saved = UserSavedNews(iduser=id_user, idnews=id_new)
        db.session.add(new_user_saved)
        db.session.commit()
        
def is_update(fecha_actual: str) -> bool:
    print("entra en is_update")
    fecha_db = db.session.query(New.date).order_by(desc(New.date)).first()[0].strftime("%Y-%m-%d")
    print(f"{fecha_db == fecha_actual}")
    return fecha_actual == str(fecha_db)

def last_id() -> int:
    latest_new = db.session.query(New).order_by(desc(New.id)).first()
    if latest_new:
        return latest_new.id
    else:
        return 0
    
#Lo podemos dejar en el manager, pero estoy probando otras cosas antes 
def transform_images_to_base64(photo_bytes):
    pil_image = Image.open(BytesIO(photo_bytes))
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    base64_image = base64.b64encode(photo_bytes).decode('utf-8')
    return base64_image