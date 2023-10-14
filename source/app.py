from flask import Flask, render_template, request, flash
from modules import web_scrapping as ws, users, filter as f, classes as cl
from flask_sqlalchemy import SQLAlchemy
from database import DBManager as manager#, Admin
from typing import List


db = manager.db
app = Flask(__name__)

app.secret_key = '1jn21rc1#kj42h35k%@24ic1ucmo4r1cni4y1@@91ch24i5nc1248591845715'

news: List[cl.News]


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
        return start()


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


# ESTE METODO Y EL SIGUIENTE ES EL MISMO ASI QUE DEBERIAN SER 1
# Guardar un usuario desde la web a la base, usando el modelo de usuario
# He cambiado el nombre del metodo: no puede tener mayusculas
@app.route('/save_commonuser', methods=['POST'])
def save_cu():
    if cl.validate_password(request.form['password']):
        # hashed_password = generate_password_hash(request.form['password'], method='sha256')
        new_user = users.Commonuser(request.form['username'], request.form['password'], request.form['email'], request.form['c_user_name'], request.form['c_user_lastname'])
        # He cambiado el nombre de la variable: no puede tener mayusculas
        new_g_user = users.User(request.form['username'], request.form['password'], request.form['email'])
        db.session.add(new_g_user)
        db.session.add(new_user)
        db.session.commit()
    
        return index()
    else:
        print("CONTRASEÑA DÉBIL")
        flash('CONTRASEÑA DÉBIL', 'WARNING')
        return register_funct()


# He cambiado el nombre del metodo: no puede tener mayusculas
@app.route('/save_companyuser', methods=['POST'])
def save_cmpu():
    if cl.validate_password(request.form['password']):
        # hashed_password = generate_password_hash(request.form['password'], method='sha256')
        # certification = 'certification' in request.form
        new_user = users.Companyuser(request.form['username'], request.form['password'], request.form['email'], request.form['company_name'], request.form['company_nif'])
        # He cambiado el nombre de la variable: no puede tener mayusculas
        new_g_user = users.User(request.form['username'], request.form['password'], request.form['email'])
        db.session.add(new_g_user)
        db.session.add(new_user)
        db.session.commit()

        return index()

    else:
        print("CONTRASEÑA DÉBIL")
        flash('CONTRASEÑA DÉBIL', 'WARNING')
        return register_funct()


# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3307/truthpaper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#db.init_app(app)

# print(Admin.load_admin())

if __name__ == '__main__':
    ws.save_html(["https://www.lasexta.com/noticias/", "https://www.antena3.com/noticias/", "https://www.marca.com/", "https://www.nytimes.com/international/"])
    app.run(debug=True)

"""
@app.route('/save_admin', methods=['POST'])
def save_admin():
        new_g_user = Admin.admin(request.form['username'], request.form['password'], request.form['email'])
        db.session.add(new_g_user)
        db.session.commit()
        return register_funct()
"""

