# Importar los módulos necesarios
from flask import Flask, render_template, request, flash, redirect, url_for, send_file, session
from modules import web_scrapping as ws, filter as f, classes as cl, graphs as gr, usermappers, entitymappers, session_data as ses
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from typing import List, Dict
import threading
from datetime import datetime
from random import *
from werkzeug.utils import secure_filename
import os


db = manager.db
app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=source/DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "ireallywanttostayatyourhouse"
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "noreply.truthpaper@gmail.com"
app.config['MAIL_PASSWORD'] = "bjkr glyc cquj icib"

mail = Mail(app)
news: List[cl.News] = []
containers: Dict[int, List[cl.News]] = {}
init_news = threading.Thread(target=ws.get_news_db, args=(app, news, containers))
semaphore = threading.Semaphore(1)
app.secret_key = 'truthpaper'  # Clave secreta para flash (alerts errores)


@app.route('/index')
def index():
    global news
    global containers
    print("llega")
    init_news.join()
    semaphore.release()

    categories = gr.get_categories(news)  # una lista
    categories_list = gr.get_general_categories(categories)
    categories_list_unique = list(set(categories_list))
    print(categories_list_unique)
    return render_template('indexFunc.html', data=news, containers=containers, categories_list_unique=categories_list_unique)


@app.route('/')
def start():
    global news, containers
    
    if not news:
        semaphore.acquire()
        if news:
            return render_template('login.html')
        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        init_news.start()
        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        if not entitymappers.is_update(datetime.now().strftime(f'%Y-%m-%d')):
            print("SE ACTUALIZAN LAS NOTICIAS")
            threading.Thread(target=_add_news_background).start()
    return render_template('login.html')


def _add_news_background():
    global news, containers
    new_news = ws.get_news()
    print("pasa")
    news += new_news #.extend(new_news)

    with app.app_context():
        # containers += ws.get_containers(new_news, app)
        # containers += dict(ws.get_containers(new_news, app))
        # containers.update(ws.get_containers(new_news, app))
        containers.update(ws.get_containers(new_news))
        # entitymappers.Container.add_container(app, new_news)
        entitymappers.Container.add_container(new_news)
        # entitymappers.New.save_news(app, new_news)
        entitymappers.New.save_news(new_news)


@app.route('/login_users', methods=['POST'])
def login_users():
    respuesta_login = usermappers.User.login(request.form['username'], request.form['password'])
    try:
        if type(respuesta_login) == bool and respuesta_login == True:
            mapped_user = usermappers.User.find_user_by_username_or_email(request.form['username'])
            ses.s_login(mapped_user.id)
            return index()
        elif type(respuesta_login) != bool and respuesta_login == 'admin':
            # Se tiene que meter en index para que se carguen las noticias
            return render_template('userAdmin/profileAdmin.html')
        else:
            flash("Datos introducidos incorrectos", "error")
            print("Datos introducidos incorrectos en el login")
            return redirect(url_for('start'))
    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {str(e)}")
        flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo de nuevo más tarde.", "error")
        return redirect(url_for('start'))


@app.route('/ver_contenedor/<int:id>')
def expand_container(id):
    container = containers.get(id)
    entitymappers.Comment.increment_views(id) # Se incrementan los views a uno de la noticia

    comments = entitymappers.Comment.load_comments(id)
    data = {'content': [comment.get_content() for comment in comments],
            'id': [comment.get_id() for comment in comments],
            'likes': [comment.get_likes() for comment in comments],
            'views': [comment.get_views() for comment in comments],
            'img': [entitymappers.Comment.load_image_comment(comment.get_id()) for comment in comments],
            'userclient_id': [comment.get_userclient_id() for comment in comments],
            'container_id': [comment.get_containerid() for comment in comments],
            'username': [usermappers.User.get_username(comment.get_userclient_id()) for comment in comments],
            'userimage': [usermappers.Userclient.load_image(comment.get_userclient_id()) for comment in comments],
            }

    if comments is None:
        return render_template('containerNews.html', container=container, id_contenedor=id)

    else:
        return render_template('containerNews.html', container=container, data=data, id_contenedor=id)


@app.route('/like_news', methods=['POST'])
def like_news():
    new_id = request.form.get('news_id')
    print(f"Se ha dado like a la noticia con ID {new_id}")
    liked_new = entitymappers.New.get_new_by_id(new_id)
    if liked_new:
        entitymappers.New.increment_likes(int(new_id))
        print("Se ha incrementado el número de likes de la noticia")
    else:
        print("No se ha podido dar like a la noticia con ID {news_id}")
    id_container = liked_new.container_id
    news = entitymappers.New.get_news_by_container_id(id_container)

    comments = entitymappers.Comment.load_comments(id_container)
    data = {'content': [comment.get_content() for comment in comments],
            'id': [comment.get_id() for comment in comments],
            'likes': [comment.get_likes() for comment in comments],
            'views': [comment.get_views() for comment in comments],
            'img': [entitymappers.Comment.load_image_comment(comment.get_id()) for comment in comments],
            'userclient_id': [comment.get_userclient_id() for comment in comments],
            'container_id': [comment.get_containerid() for comment in comments],
            'username': [usermappers.User.get_username(comment.get_userclient_id()) for comment in comments],
            'userimage': [usermappers.Userclient.load_image(comment.get_userclient_id()) for comment in comments],
            }

    return render_template('containerNews.html', container=news, id_contenedor=id_container, data=data)



@app.route('/like_comment', methods=['POST'])
def like_comment():
    global comments
    comment_id = request.form.get('comment_id')
    print(f"Se ha dado like al comentario con ID {comment_id}")
    comment = entitymappers.Comment.get_comment_by_id(comment_id)
    if comment is not None:
        entitymappers.Comment.comment_likes(int(comment_id))
        print("Se ha incrementado el número de likes del comentario")
    else:
        print("No se ha podido dar like al comentario con ID {comment_id}")
    id_container = comment.container_id
    return redirect(url_for('expand_container', id=id_container))


@app.route('/publish_comment', methods=['POST'])
def publish_comment():
    user_id = ses.get_user_id()
    container_id = request.form.get('container_id')
    content = request.form.get('content')

    # Manejar la carga de la imagen
    file = request.files['image']
    if file and allowed_file(file.filename):
        image_bytes = file.read()
    else:
        image_bytes = None
    comment_id = entitymappers.Comment.insert_comment(user_id, container_id, content, image_bytes)
    print(f"Se ha insertado el comentario con ID {comment_id}")

    return redirect(url_for('expand_container', id=container_id))


# Función que muestra una categoría general compuesta por N específicas
@app.route('/category/<string:general_category>')
def expand_category(general_category):
    global news
    global containers
    #print("categoría: " + general_category)
    # category --> categoria general
    categories_list = gr.get_specific_categories(general_category)
    print(categories_list)
    filtered_news = f.filter_by_categories(categories_list, news)
    if len(filtered_news) < 1:
        print("No hay noticias de esa categoría")
    else:
        print("Hay noticias de esa categoría")

    return render_template('categoriesFunc.html', news=filtered_news, containers=containers,
                           category=general_category)


@app.route('/register.html')
def register_funct():
    return render_template('register.html')


@app.route('/login_back')
def go_to_login():
    return render_template('login.html')


def mostrar_perfil_usuarios(user_id, user_name):
    user_image = usermappers.Userclient.load_image(user_id)
    user_email = usermappers.User.get_user_email(user_id)
    return render_template('perfil.html', user_id=user_id, user_name=user_name, user_image=user_image,
                           user_email=user_email)


@app.route('/perfil')
def go_to_profile():
    user_id = ses.get_user_id()
    user_name = usermappers.User.get_user_name(user_id)
    return mostrar_perfil_usuarios(user_id, user_name)


@app.route('/termsandConditions')
def termsConditions():
    return render_template('termsConditions.html')


@app.route('/categories')
def go_to_categories():
    return render_template('categories.html')


@app.route('/login_admin')
def go_to_admin():
    return render_template('loginAdmin.html')





@app.route('/save_keyword', methods=['post'])
def save_keyword():
    keyword = request.form['search']
    global news
    filtered_news = f.filter_by_words(keyword, news)

    return render_template('categories.html', news = filtered_news)



def handle_user_registration(user_type):
    global unverified_email
    result = usermappers.User.save_user()
    if result == -1:
        return render_template('register.html', registration_error="Contraseña débil", form=request.form)
    elif result == -2:
        return render_template('register.html', registration_error="Email inválido", form=request.form)
    elif result == -3:
        return render_template('register.html', registration_error="Nombre de usuario/email ya existente",
                               form=request.form)
    else:
        unverified_email = request.form['email']
        if user_type == 'common':
            if usermappers.Commonuser.save_commonuser(result):
                return send_email(unverified_email, False)
        elif user_type == 'company':
            if usermappers.Companyuser.save_companyuser(result):
                return send_email(unverified_email, False)
        elif user_type == 'journalist':
            if usermappers.Journalistuser.save_journalistuser(result):
                return send_email(unverified_email, False)
        else:
            # Manejar un tipo de usuario no válido, si es necesario
            pass


@app.route('/save_commonuser', methods=['POST'])
def register_user_common():
    return handle_user_registration('common')


@app.route('/save_companyUser', methods=['POST'])
def register_user_company():
    return handle_user_registration('company')


@app.route('/save_journalistUser', methods=['POST'])
def register_user_journalist():
    return handle_user_registration('journalist')


# Métodos para el ADMINISTRADOR
@app.route('/indexAdmin')
def index_admin():
    unchecked_users = usermappers.Userclient.loadUncheckedUsers()
    return render_template('userAdmin/indexAdmin.html', unchecked_users=unchecked_users)


@app.route('/verifyUsers')
def verify_users():
    unchecked_users = usermappers.Userclient.loadUncheckedUsers()
    # Si el user_id de algun unchecked_user está en la tabla journalistusers, se devuelve True
    '''
    for user in unchecked_users:
        if(manager.is_journalist(user[3])):
            user.append(True)
        else:
            user.append(False)
    '''
    print("Unchecked Users: " + str(unchecked_users))
    return render_template('userAdmin/verifyUsers.html', unchecked_users=unchecked_users)


# Método para verificar a los usuarios (Y: cambiar el estado de is_checked a 'Y')
@app.route('/process_verification', methods=['POST'])
def process_verification():
    user_id = request.form.get('user_id')
    action = request.form.get('action')  # 'accept' or 'deny'
    if action == 'accept':
        print("===================ACCEPT USER===================")
        usermappers.Userclient.updateUserChecked(user_id)
    return redirect('/verifyUsers')


@app.route('/pdfReader/<int:user_id>')  # id del usuario
def pdf_reader(user_id):
    # Enviar pdf según el id del usuario
    pdf = usermappers.Journalistuser.load_pdf_certificate(user_id)
    return render_template('userAdmin/pdfReader.html', pdf=pdf)


@app.route('/charts')
def charts():
    categorias = gr.get_categories(news)
    return render_template('userAdmin/charts.html', categorias=categorias)


# Función que genera el gráfico de noticias/fuente
@app.route('/generate_chart_source', methods=['POST'])
def generate_charts_source():
    gr.graph_news_per_source(news)
    return redirect(url_for('charts'))


# Función que genera l gráfico de noticias/categorias
@app.route('/generate_chart_category', methods=['POST'])
def generate_chart_category():
    gr.graph_news_per_category(news)
    return redirect(url_for('charts'))


# Función que genera la nube de palabras
@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    categoria = request.form['categoria']  # Obtener la categoría seleccionada del formulario
    gr.wordcloud_per_category(news, categoria)
    return redirect(url_for('charts'))


@app.route('/comments')
def comments():
    return render_template('userAdmin/comments.html')


@app.route('/editUsers')
def edit_users():
    return render_template('userAdmin/editUsers.html')

@app.route('/profileAdmin')
def profile_admin():
    return render_template('userAdmin/profileAdmin.html')

# NOTICIAS GUARDADAS

def generate_code():
    code = randint(000000, 999999)
    return code


def send_email(email, repeat):
    global email_code
    email_code = generate_code()
    msg_title = "BIENVENID@ a TRUTHPAPER"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[email])
    msg_body = "Introduzca el código a continuación para confirmar su dirección de correo electrónico. Si no creó una cuenta con TruthPaper, puede eliminar este correo electrónico de forma segura."
    msg.body = ""
    data = {
        'app_name': "TRUTHPAPER",
        'title': msg_title,
        'body': msg_body,
        'code': email_code
    }

    msg.html = render_template("email.html", data=data)

    try:
        mail.send(msg)
        if repeat:
            return render_template('validation.html', validation_error="Otro envío")
        else:
            return render_template('validation.html')
    except Exception as e:
        print(e)
        return render_template('register.html', registration_error="Error verificación")


@app.route('/validation')
def validation():
    return render_template('validation.html')


@app.route('/send_email_again')
def send_email_again():
    return send_email(unverified_email, True)


@app.route('/verify_email', methods=['POST'])
def verify_email():
    user_code = request.form['password']
    print("USER -> ", user_code, type(user_code))
    print("EMAIL -> ", email_code, type(email_code))
    if int(user_code) == int(email_code):
        usermappers.User.updateUserVerified(unverified_email)
        return render_template('verifyEmail.html')
    else:
        return render_template('validation.html', validation_error="Código incorrecto")


@app.route('/savedNews')
def go_to_savedNews():
    # Carga los Id's de las noticias guardadas por el usuario en sesion
    id_saved_news = entitymappers.UserSavedNews.load_ids_news_saved_by_user(ses.get_user_id()) 
    news_saved = entitymappers.New.load_news_by_id(id_saved_news)
    return render_template('SavedNews.html', news = news_saved)

@app.route('/save_news', methods=['POST'])
def save_news():
    # print("se ha activado el método de guardar noticias")
    news_id = request.form.get('news_id')
    entitymappers.UserSavedNews.user_saves_a_new(id_user=ses.get_user_id(), id_new=news_id)
    return go_to_savedNews()

@app.route('/delete_news', methods=['POST'])
def delete_news():
    news_id = request.form.get('news_id')
    entitymappers.UserSavedNews.user_deletes_a_new(id_user=ses.get_user_id(), id_new=news_id)
    return go_to_savedNews()



#@app.route('/savedNews')
# def upload_saved_news():
#     user_id = USER_ID_SESION
#     id_saved_news = entitymappers.UserSavedNews.load_saved_news(user_id) # Carga los ids de las noticias guardadas
#     news_saved = entitymappers.New.load_news_by_id(id_saved_news) # Carga las noticias con los ids anteriores
#  #   return news_saved
#     return render_template('SavedNews.html', news = news_saved)

# MySQL Connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=DigiCertGlobalRootCA.crt.pem'

# Configuración para subir imágenes en comentarios
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db.init_app(app)

if __name__ == '__main__':
    # ws.save_html()
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=4000)
