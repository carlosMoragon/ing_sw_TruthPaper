# Importar los módulos necesarios

from flask import Flask, render_template, request, flash, redirect,url_for, send_file
from modules import web_scrapping as ws, users, filter as f, classes as cl, graphs as gr
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict
import threading
from datetime import datetime
#import fitz
from io import BytesIO
#from pdf2image import convert_from_bytes

db = manager.db
app = Flask(__name__)

news: List[cl.News] = []
containers: Dict[int, List[cl.News]] = {}
init_news = threading.Thread(target=ws.get_news_db, args=(app, news, containers))
app.secret_key = 'truthpaper' # Clave secreta para flash (alerts errores)


@app.route('/index')
def index():
    global news
    global containers
    print("llega")
    init_news.join()
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

@app.route('/')
def start():
     global news, containers
     if not news:
        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        init_news.start()
        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        if not manager.is_update(datetime.now().strftime(f'%Y-%m-%d')):
            print("SE ACTUALIZAN LAS NOTICIAS")
            threading.Thread(target=_add_news_background).start()
     return render_template('login.html')


def _add_news_background():
    global news, containers
    new_news = ws.get_news()
    news.extend(new_news)
    containers = ws.get_containers(news, app)
    manager.add_container(app, new_news)
    manager.save_news(app, new_news)


# CAMBIAR LA RUTA
'''
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

'''
@app.route('/login_users', methods=['POST'])
def login_users():
    respuesta_login = manager.login(request.form['username'], request.form['password'])
    try:
        if (type(respuesta_login) == bool and respuesta_login == True):
            return index()
        elif (type(respuesta_login) != bool):
            return 'Yes bae'
        else:
            flash("Datos introducidos incorrectos", "error")
            print("datos introducidos incorrectos")
            return redirect(url_for('start'))
    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {str(e)}")
        flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo de nuevo más tarde.", "error")
        return redirect(url_for('start'))

@app.route('/ver_contenedor/<int:id>')
def expand_container(id):
    container = containers.get(id)

    comments = manager.load_comments(id)
    data = {
        'content': [comment.get_content() for comment in comments],
        # 'username': [manager.get_username(comment.get_userclient_id) for comment in comments], # NO FUNCIONA
        'id': [comment.get_id() for comment in comments],
        'likes': [comment.get_likes() for comment in comments],
        'views': [comment.get_views() for comment in comments],
        'img': [comment.get_img() for comment in comments],
        'userclient_id': [comment.get_userclient_id() for comment in comments],
        'container_id': [comment.get_containerid() for comment in comments]
    }
    if comments is None:
        return render_template('containerNews.html', container=container)
    else:
        return render_template('containerNews.html', container=container, data=data, id_contenedor=id)

@app.route('/like_news', methods=['POST'])
def like_news():
    global news
    news_id = request.form.get('news_id')
    print(f"Se ha dado like a la noticia con ID {news_id}")
    new = manager.get_new_by_id(news_id)
    if new is not None:
        manager.increment_likes(int(news_id))
        print("Se ha incrementado el número de likes de la noticia")
    else:
        print("No se ha podido dar like a la noticia con ID {news_id}")
    id_container = new.container_id
    for new in news:
        if new.get_id() == id_container:
            new.set_likes(new.get_likes()+1)
            break
    return redirect(url_for('expand_container', id=id_container))

@app.route('/like_comment', methods=['POST'])
def like_comment():
    global comments
    comment_id = request.form.get('comment_id')
    print(f"Se ha dado like al comentario con ID {comment_id}")
    comment = manager.get_comment_by_id(comment_id)
    if comment is not None:
        manager.comment_likes(int(comment_id))
        print("Se ha incrementado el número de likes del comentario"  )
    else:
        print("No se ha podido dar like al comentario con ID {comment_id}")
    id_container = comment.container_id
    return redirect(url_for('expand_container', id=id_container))

@app.route('/publish_comment', methods=['POST'])
def publish_comment():
    user_id = 11 # CAMBIAR POR EL ID DEL USUARIO QUE ESTÉ LOGUEADO
    container_id = request.form.get('container_id')
    content = request.form.get('content')

    comment_id = manager.insert_comment(user_id, container_id, content)
    print(f"Se ha insertado el comentario con ID {comment_id}")

    return redirect(url_for('expand_container', id=container_id))

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

@app.route('/register.html')
def register_funct():
    return render_template('register.html')

@app.route('/login_back')
def go_to_login():
    return render_template('login.html')

@app.route('/perfil')
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

