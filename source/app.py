# Importar los módulos necesarios

from flask import Flask, render_template, request, flash, redirect, url_for, send_file, session
from modules import web_scrapping as ws, filter as f, classes as cl, graphs as gr, usermappers, entitymappers
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict
import threading
from datetime import datetime
from werkzeug.utils import secure_filename
import os


usuarios_en_sesion = cl.UsersInSession()
#anaMencionoUnIdDeSesion
global USER_ID_SESION #Se inicializa en login_users
    
db = manager.db
app = Flask(__name__)

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

    # for new in news:
    #     print(f"{new.get_container_id()}\n")
    data = {
        'imgs': [new.get_image() for new in news],
        'titles': [str(new.get_title()) for new in news],
        'urls': [new.get_url() for new in news],
        'dates': [new.get_date() for new in news],
        'categories': [new.get_category() for new in news],
        'likes': [new.get_likes() for new in news],
        'views': [new.get_views() for new in news]
    }
    categories = gr.get_categories(news)  # una lista
    categories_list = gr.get_general_categories(categories)
    categories_list_unique = list(set(categories_list))
    print(categories_list_unique)
    return render_template('indexFunc.html', data=data, containers=containers, categories_list_unique=categories_list_unique)


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
    # containers += ws.get_containers(new_news, app)
    # containers += dict(ws.get_containers(new_news, app))
    containers.update(ws.get_containers(new_news, app))

    entitymappers.Container.add_container(app, new_news)
    entitymappers.New.save_news(app, new_news)


@app.route('/login_users', methods=['POST'])
def login_users():
    respuesta_login = usermappers.User.login(request.form['username'], request.form['password'])
    try:
        if type(respuesta_login) == bool and respuesta_login == True:

            mapped_user = usermappers.User.getAllUserData(request.form['username']) 
            USUARIO_EN_SESION = cl.UserInApp(mapped_user.id, mapped_user.username, mapped_user.password, mapped_user.email) #No interesa mucho mapear la contraseña
            usuarios_en_sesion.add_user(USUARIO_EN_SESION)    
            global USER_ID_SESION #Cutre... ya lo se 
            USER_ID_SESION = USUARIO_EN_SESION.get_id()

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
    entitymappers.Comment.increment_views(id) # Se incrementan los likes a uno de la noticia

    comments = entitymappers.Comment.load_comments(id)
    data = {'content': [comment.get_content() for comment in comments],
            'id': [comment.get_id() for comment in comments],
            'likes': [comment.get_likes() for comment in comments],
            'views': [comment.get_views() for comment in comments],
            'img': [entitymappers.Comment.load_image_comment(comment.get_id()) for comment in comments],
            'userclient_id': [comment.get_userclient_id() for comment in comments],
            'container_id': [comment.get_containerid() for comment in comments]
            }

    if comments is None:
        return render_template('containerNews.html', container=container, id_contenedor=id)

    else:
        return render_template('containerNews.html', container=container, data=data, id_contenedor=id)


@app.route('/like_news', methods=['POST'])
def like_news():
    global news
    news_id = request.form.get('news_id')
    print(f"Se ha dado like a la noticia con ID {news_id}")
    new = entitymappers.New.get_new_by_id(news_id)
    if new is not None:
        entitymappers.New.increment_likes(int(news_id))
        print("Se ha incrementado el número de likes de la noticia")
    else:
        print("No se ha podido dar like a la noticia con ID {news_id}")
    id_container = new.container_id
    for new in news:
        if new.get_container_id() == id_container:
            new.set_likes(new.get_likes() + 1)
            break
    return redirect(url_for('expand_container', id=id_container))


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
    user_id = 11  # CAMBIAR POR EL ID DEL USUARIO QUE ESTÉ LOGUEADO
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
    print("categoría: " + general_category)
    # category --> categoria general
    categories_list = gr.get_specific_categories(general_category)
    print(categories_list)
    filtered_news = f.filter_by_categories(categories_list, news)
    if len(filtered_news) < 1:
        print("No hay noticias de esa categoría")
    else:
        print("Hay noticias de esa categoría")

    data = {
        'imgs': [new.get_image() for new in filtered_news],
        'titles': [str(new.get_title()) for new in filtered_news],
        'urls': [new.get_url() for new in filtered_news],
        'dates': [new.get_date() for new in filtered_news],
        'categories': [new.get_category() for new in filtered_news],
        'likes': [new.get_likes() for new in filtered_news],
        'views': [new.get_views() for new in filtered_news]
    }
    print(data['categories'])

    return render_template('categoriesFunc.html', data=data, news=filtered_news, containers=containers,
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
    return render_template('perfil.html', user_id=user_id, user_name=user_name, user_image=user_image, user_email = user_email)


@app.route('/perfil')
def go_to_profile():
    #print("User id: " + str(USER_ID_SESION))
    usuario_actual = usuarios_en_sesion.get_user_by_id(USER_ID_SESION)
    user_name = usuario_actual.get_username()
    return mostrar_perfil_usuarios(USER_ID_SESION, user_name)


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
    filted_news = f.filter_by_words(keyword, news)
    data = {
        'imgs': [new.get_image() for new in filted_news],
        'titles': [new.get_title() for new in filted_news],
        'urls': [new.get_url() for new in filted_news],
        'keyword': keyword,
        'dates': [new.get_date() for new in filted_news],
        'categories': [new.get_category() for new in filted_news],
        'likes': [new.get_likes() for new in filted_news],
        'views': [new.get_views() for new in filted_news]
    }
    return render_template('categoriesFunc.html', data=data)


def handle_user_registration(user_type):
    result = usermappers.User.save_user()
    if result == -1:
        return render_template('register.html', registration_error="Contraseña débil", form=request.form)
    elif result == -2:
        return render_template('register.html', registration_error="Email inválido", form=request.form)
    elif result == -3:
        return render_template('register.html', registration_error="Nombre de usuario/email ya existente", form=request.form)
    else:
        if user_type == 'common':
            if usermappers.Commonuser.save_commonuser(result):
                return index()
        elif user_type == 'company':
            if usermappers.Companyuser.save_companyuser(result):
                return index()
        elif user_type == 'journalist':
            if usermappers.Journalistuser.save_journalistuser(result):
                return index()
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
    # Habrñia que cargar las noticias porque si no entras en index no se cargan
    # opción 1: cargarlas aquí
    # opción 2: Index >> botón: Usuario Admin >> indexAdmin
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


@app.route('/pdfReader/<int:user_id>') # id del usuario
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



# MySQL Connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=DigiCertGlobalRootCA.crt.pem'

# Configuración para subir imágenes en comentarios
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=source/DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

if __name__ == '__main__':
    # ws.save_html()
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=4000)
