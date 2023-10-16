from flask import Flask, render_template, request, flash
from modules import web_scrapping as ws, users, filter as f, classes as cl, graphs as gr
from database import DBManager as manager
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict

db = manager.db
#admin_user = AdminUser('admin', '1234', 'adminUser@truthpaper.com', True, True, True)

app = Flask(__name__)

news: List[cl.News]
containers: Dict[int, List[cl.News]]
# init_news = threading.Thread(target=manager.get_news_db)

@app.route('/index')
def index():
    global news
    news = ws.get_news()

    data = {
        'imgs': [new.get_image() for new in news],
        'titles': [str(new.get_title()) for new in news],
        'urls': [new.get_url() for new in news],
        'dates': [new.get_date() for new in news],
        'categories': [new.get_category() for new in news]
    }
    print(news[0].get_image())
    return render_template('indexFunc.html', data=data)


@app.route('/')
def start():
    # global news, containers
    # if news is None:
        # ESTA ES LA DE LAS BBDD QUE SON LAS QUE MAS RAPIDO TIENEN QUE IR
        # results = init_news.start()
        # news = results[0]
        # containers = results[1]

        # ESTAS SON LAS QUE SON NUEVAS QUE SE VAN A IR AÑADIENDO A LO LARGO DE LA EJECUCION
        # threading.Thread(target=_add_news_background).start()

    return render_template('login.html')


def _add_news_background():
    global news, containers
    news += ws.get_news()
    containers = ws.get_containers(news)


# CAMBIAR LA RUTA
@app.route('/login_users', methods=['POST'])
def login_users():
    if manager.login(request.form['username'], request.form['password']):
        return index()
    else:
        return render_template('error_login.html')

@app.route('/register.html')
def register_funct():
    return render_template('register.html')


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
    return render_template('categoriasFunc.html', data=data)


@app.route('/pruebaArticulos')
def prueba_articulos():
    global news
    # news = ws.get_news()
    data = {
        'imgs' : [new.get_image() for new in news],
        'titles' : [new.get_title() for new in news],
        'urls' : [new.get_url() for new in news]
    }   
    return render_template('pruebaArticulos.html', data=data)

#Aun en PROCESO se MEJORA y DEPURACIÓN

@app.route('/save_commonuser', methods=['POST'])
def register_user():
    result = manager.save_user() 
    if result == False: 
        return render_template('fail_register.html')
    else:
        if manager.save_commonuser(result):
            return index()


@app.route('/save_companyUser', methods=['POST'])
def register_CompanyUser():
    result = manager.save_user() 
    if result == False: 
        return render_template('fail_register.html')
    else:
        if manager.save_companyuser(result):
            return index()
    
    
@app.route('/save_journalistUser', methods=['POST'])
def register_JournalistUser():
    result = manager.save_user() 
    if result == False: 
        return render_template('fail_register.html')
    else:
        if manager.save_journalistuser(result):
            return index()

#Métodos para el ADMINISTRADOR
@app.route('/userAdmin.html')
def index_admin():
    noticias = ws.get_news()
    gr.graph_news_per_source(noticias)
    return render_template('userAdmin/indexAdmin.html')

@app.route('/verifUsers')
def verify_users():
    return render_template('userAdmin/verifyUsers.html')

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

