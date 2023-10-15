from flask import Flask, render_template, request, flash
from modules import web_scrapping as ws, users, filter as f, classes as cl
from database import DBManager as manager
from typing import List
from flask_sqlalchemy import SQLAlchemy

db = manager.db
#admin_user = AdminUser('admin', '1234', 'adminUser@truthpaper.com', True, True, True)

app = Flask(__name__)

news: List[cl.News]

@app.route('/index')
def index():
    global news
    news = ws.get_news()
    data = {
        'imgs': [new.get_image() for new in news],
        'titles': [str(new.get_title()) for new in news],
        'urls': [new.get_url() for new in news],
        'dates': [new.get_date() for new in news]
    }

    return render_template('indexFunc.html', data=data)


@app.route('/')
def start():
    return render_template('login.html')


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
        'dates': [new.get_date() for new in filted_news]
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
    if manager.save_commonuser():
        return index()
    else:
        return render_template('fail_register.html')
   
@app.route('/save_companyuser', methods=['POST'])
def register_Cuser():
    if manager.save_cmpu():
        return index()
    else:
        return render_template('fail_register.html')



# MySQL Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=source\\DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#print(admin_user.loadUncheckedUsers())

if __name__ == '__main__':
    #ws.save_html()
    app.run(debug=True)


