from flask import Flask, render_template, request, flash, redirect, send_file
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
init_news = threading.Thread(target=manager.get_news_db, args=(app, news, containers))


@app.route('/index')
def index():
    global news
    global containers
    print("llega")
    init_news.join()
    data = {
        'imgs': [new.get_image() for new in news],
        'titles': [str(new.get_title()) for new in news],
        'urls': [new.get_url() for new in news],
        'dates': [new.get_date() for new in news],
        'categories': [new.get_category() for new in news]
    }

    return render_template('indexFunc.html', data=data, containers=containers)

#Método para ver un contenedor específico
@app.route('/ver_contenedor/<int:id>')
def expand_container(id):
    container = containers.get(id)
    return render_template('containerNews.html', container=container)

@app.route('/')
def start():
     global news, containers
     if not news:

        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        init_news.start()

        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        if manager.is_update(datetime.now().strftime(f'%Y-%m-%d')):
            threading.Thread(target=_add_news_background).start()

    #SON PRUEBAS, SIRVEN PARA VER ESTOS DATOS POR CONSOLA
    # lista = manager.loadUncheckedUsers()
    #  lista = manager.load_new()
    #  for i in lista:
    #      print(i)

     return render_template('login.html')


def _add_news_background():
    global news, containers
    new_news = ws.get_news()
    news.extend(new_news)
    containers = ws.get_containers(news)
    manager.save_news(app, new_news)


# def convert_pdf_to_images(pdf_bytes):
#     images = convert_from_bytes(pdf_bytes)
#     return images

# CAMBIAR LA RUTA
@app.route('/login_users', methods=['POST'])
def login_users(): 
    if manager.login(request.form['username'], request.form['password']):
        user = users.User.query.filter_by(username=request.form['username']).first()
        client_id = user.id
        image = manager.load_image(client_id)
        return image
        
        # user = users.User.query.filter_by(username=request.form['username']).first()
        # journalist_id = user.id       
        # documento = manager.load_pdf_certificate(journalist_id)
        # return manager.serve_pil_image(documento)
        
        #return index()
    else:
        return render_template('fail_login.html')

@app.route('/register.html')
def register_funct():
    return render_template('register.html')

@app.route('/login_back')
def go_to_login():
    return render_template('login.html')

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
        'categories': [new.get_category() for new in filted_news]
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
   
def handle_user_registration(user_type):
    result = manager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
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
    #noticias = news
    #gr.graph_news_per_source(noticias)
    return render_template('userAdmin/indexAdmin.html')

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
    return render_template('userAdmin/charts.html')

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

