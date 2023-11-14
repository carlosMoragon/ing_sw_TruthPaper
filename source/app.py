# Importar los módulos necesarios

from flask import Flask, render_template, request, flash, redirect,url_for, send_file
from modules import web_scrapping as ws, users, filter as f, classes as cl, graphs as gr
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict
import threading
from datetime import datetime
from pdf2image import convert_from_bytes

db = manager.db
app = Flask(__name__)

news: List[cl.News] = []
containers: Dict[int, List[cl.News]] = {}
init_news = threading.Thread(target=manager.get_news_db, args=(app, news, containers))
app.secret_key = 'truthpaper' # Clave secreta para flash (alerts errores)


@app.route('/index')
def index():
    global news
    global containers
    print("llega")
    #init_news.join()
    for new in news:
        print(f"{new.get_container_id()}\n")
    data = {
        'imgs': [new.get_image() for new in news],
        'titles': [str(new.get_title()) for new in news],
        'urls': [new.get_url() for new in news],
        'dates': [new.get_date() for new in news],
        'categories': [new.get_category() for new in news],
        'likes': [new.get_likes() for new in news],
        'views': [new.get_views() for new in news]
    }
    categories = gr.get_categories(news) # una lista
    categories_list = gr.get_general_categories(categories)
    categories_list_unique = list(set(categories_list))
    return render_template('indexFunc.html', data=data, containers=containers, categories_list=categories_list_unique)

# Método para ver un contenedor específico
@app.route('/ver_contenedor/<int:id>')
def expand_container(id):
    container = containers.get(id)
    comments = manager.load_comments(id)
    data = {
        'content': [comment.get_content() for comment in comments],
        'username': [manager.get_username(comment.get_userclient_id()) for comment in comments],
        'id': [comment.get_id() for comment in comments],
        'likes': [comment.get_likes() for comment in comments],
        'views': [comment.get_views() for comment in comments],
        'img': [comment.get_img() for comment in comments],
    }
    if comments is None:
        return render_template('containerNews.html', container=container)
    return render_template('containerNews.html', container=container, data=data)
''' comments
data = {
        'content': [comment.get_content() for comment in comments],
        'username': [manager.get_username(comment.get_userclient_id) for comment in comment],
        'id': [comment.get_id() for comment in comments],
        'likes': [comment.get_likes() for comment in comments],
        'views': [comment.get_views() for comment in comments],
        'img': [comment.get_img() for comment in comments],
        'userclient_id': [comment.get_userclient_id() for comment in comments],
        'container_id': [comment.get_container_id() for comment in comments]
    }
    
    En el HTML pondremos
    Nombre usuario: {{data.username}}
    Contenido: {{data.content}}
    Likes: {{data.likes}}
    Views: {{data.views}}
    
'''

# Método que inserta un comentario en un contenedor
@app.route('/insert_comment', methods=['POST'])
def insert_comment(id_container):
    comment_content = request.form.get('comment_content')
    manager.insert_comment(user_id=manager.user_id, container_id=id_container, content=comment_content)
    if manager.user_id is not None:
        # Insertar el comentario en la base de datos
        insert_comment(manager.user_id, id, comment_content)
    return redirect(url_for('expand_container', id=id_container))


# Función que muestra una categoría general compuesta por N específicas

@app.route('/category/<string:category>')
def expand_category(category):
    # category --> categoria general
    categories_list = gr.get_general_categories(category)
    print(categories_list)
    global news
    global containers
    filtered_news = f.filter_by_general_categories(categories_list, news)
    data = {
        'imgs': [new.get_image() for new in filtered_news],
        'titles': [str(new.get_title()) for new in filtered_news],
        'urls': [new.get_url() for new in filtered_news],
        'dates': [new.get_date() for new in filtered_news],
        'categories': [new.get_category() for new in filtered_news],
        'likes': [new.get_likes() for new in filtered_news],
        'views': [new.get_views() for new in filtered_news]
    }
    return render_template('categoriesFunc.html', data=data, containers=containers)
@app.route('/')
def start():
     global news, containers
     if not news:

        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        #init_news.start()

        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        if not manager.is_update(datetime.now().strftime(f'%Y-%m-%d')):
            print("SE ACTUALIZAN LAS NOTICIAS")
            threading.Thread(target=_add_news_background).start()


    #SON PRUEBAS, SIRVEN PARA VER ESTOS DATOS POR CONSOLA
    # lista = manager.loadUncheckedUsers()
    #  lista = manager.load_new()
    #  for i in lista:
    #      print(i)

     return render_template('loginAntiguo.html')


def _add_news_background():
    global news, containers
    new_news = ws.get_news()
    news.extend(new_news)
    containers = ws.get_containers(news)
    manager.add_container(app, new_news)
    manager.save_news(app, new_news)


def convert_pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images

# CAMBIAR LA RUTA
@app.route('/login_users', methods=['POST'])
def login_users():
    try:
        if manager.login(request.form['username'], request.form['password']):
            return index()
        else:
            flash("Datos introducidos incorrectos", "error")
            return redirect(url_for('start'))
    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {str(e)}")
        flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo de nuevo más tarde.", "error")
        return redirect(url_for('start'))


@app.route('/register.html')
def register_funct():
    return render_template('register.html')

@app.route('/login_back')
def go_to_login():
    return render_template('loginAntiguo.html')

@app.route('/login_back')
def go_to_profile():
    return render_template('perfil.html')

@app.route('/termsandConditions')
def termsConditions():
    return render_template('termsConditions.html')

@app.route('/categories')
def go_to_categories():
    return render_template('categories.html')


@app.route('/save_keyword', methods=['post'])
def save_keyword():
    keyword = request.form['search']
    global news
    filted_news = f.filter_by_words(keyword, news)
    data = {
        'imgs' : [new.get_image() for new in filted_news],
        'titles' : [new.get_title() for new in filted_news],
        'urls' : [new.get_url() for new in filted_news],
        'keyword': keyword,
        'dates': [new.get_date() for new in filted_news],
        'categories': [new.get_category() for new in filted_news],
        'likes': [new.get_likes() for new in filted_news],
        'views': [new.get_views() for new in filted_news]
    }
    return render_template('categoriesFunc.html', data=data)


# @app.route('/pruebaArticulos')
# def prueba_articulos():
#     global news
#     # news = ws.get_news()
#     data = {
#         'imgs' : [new.get_image() for new in news],
#         'titles' : [new.get_title() for new in news],
#         'urls' : [new.get_url() for new in news]
#     }   
#     return render_template('pruebaArticulos.html', data=data)

#Aun en PROCESO se MEJORA y DEPURACIÓN
@app.route('/save_commonuser', methods=['POST'])
def handle_user_registration(user_type):
    result = manager.save_user()
    if result == -1:
        return render_template('register.html', registration_error="Contraseña débil", form=request.form)
    elif result == -2:
        return render_template('register.html', registration_error="Email inválido", form=request.form)
    else:
        if user_type == 'common':
            if manager.save_commonuser(result):
                return index()
        elif user_type == 'company':
            if manager.save_companyuser(result):
                return index()
        elif user_type == 'journalist':
            if manager.save_journalistuser(result):
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



#Métodos para el ADMINISTRADOR
@app.route('/indexAdmin')
def index_admin():
    unchecked_users = manager.loadUncheckedUsers()
    return render_template('userAdmin/indexAdmin.html', unchecked_users=unchecked_users)

@app.route('/verifyUsers')
def verify_users():
    unchecked_users = manager.loadUncheckedUsers()
    return render_template('userAdmin/verifyUsers.html', unchecked_users=unchecked_users)

#Método para verificar a los usuarios (Y: cambiar el estado de is_checked a 'Y')
@app.route('/process_verification', methods=['POST'])
def process_verification():
    user_id = request.form.get('user_id')
    action = request.form.get('action') # 'accept' or 'deny'
    if action == 'accept':
        print("===================ACCEPT USER===================")
        manager.updateUserChecked(user_id)
    return redirect('/verifyUsers')

@app.route('/charts')
def charts():
    categorias = gr.get_categories(news)
    return render_template('userAdmin/charts.html', categorias = categorias)

#Función que genera el gráfico de noticias/fuente
@app.route('/generate_chart_source', methods=['POST'])
def generate_charts_source():
    gr.graph_news_per_source(news)
    return redirect(url_for('charts'))

#Función que genera l gráfico de noticias/categorias
@app.route('/generate_chart_category', methods=['POST'])
def generate_chart_category():
    gr.graph_news_per_category(news)
    return redirect(url_for('charts'))

#Función que genera la nube de palabras
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

@app.route('/pdfreader')
def pdf_reader():
    return render_template('userAdmin/pdfReader.html')



# MySQL Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=source\\DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


if __name__ == '__main__':
    #ws.save_html()
    app.run(debug=True)

