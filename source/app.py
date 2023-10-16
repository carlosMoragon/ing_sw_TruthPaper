from flask import Flask, render_template, request, flash, redirect
from modules import web_scrapping as ws, users, filter as f, classes as cl, graphs as gr
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict
import threading

db = manager.db
app = Flask(__name__)

news: List[cl.News] = []
containers: Dict[int, List[cl.News]] = {}
init_news = threading.Thread(target=manager.get_news_db, args=(news, containers))


@app.route('/index')
def index():
    global news
    global containers
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
        print("entra")
        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        init_news.start()

        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        threading.Thread(target=_add_news_background).start()

     # lista = manager.loadUncheckedUsers()
     # for i in lista:
     #     print(i)
     print(f"sale {news}")
     return render_template('login.html')


def _add_news_background() -> None:
     global news, containers
     news += ws.get_news()
     containers = ws.get_containers(news)
     pass


# CAMBIAR LA RUTA
@app.route('/login_users', methods=['POST'])
def login_users(): 
    if manager.login(request.form['username'], request.form['password']):
        return index()
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

#Aun en PROCESO se MEJORA y DEPURACIÓN

@app.route('/save_commonuser', methods=['POST'])
def register_user():
    result = manager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if manager.save_journalistuser(result):
            return index()


@app.route('/save_companyUser', methods=['POST'])
def register_CompanyUser():
    result = manager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if manager.save_journalistuser(result):
            return index()
    
    
@app.route('/save_journalistUser', methods=['POST'])
def register_JournalistUser():
    result = manager.save_user() 
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if manager.save_journalistuser(result):
            return index()

#Métodos para el ADMINISTRADOR
@app.route('/userAdmin.html')
def index_admin():
    noticias = ws.get_news()
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
    action = request.form.get('action') # 'accept' or 'reject'
    if action == 'accept':
        manager.updateUserChecked(user_id)
    return redirect('userAdmin/verifyUsers.html')

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

