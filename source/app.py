from flask import Flask, render_template, request
from modules import web_scrapping as ws, users, filter as f
from flask_sqlalchemy import SQLAlchemy
from database import DBManager as manager
from werkzeug.security import generate_password_hash

db = manager.db
app = Flask(__name__)

# @app.route('/')
# def index():
#     # news = f.filter_by_words("muerto", ws.get_lasextanews() + ws.get_antena3news())
#     news = ws.get_lasextanews() + ws.get_antena3news()
#     data = {
#         'imgs' : [new.get_image() for new in news],
#         'titles' : [str(new.get_title()) for new in news],
#         'urls' : [new.get_url() for new in news]
#     }

#     return render_template('indexFunc.html', data=data)


@app.route('/login')
def login():  
    manager.login(request.form['username'], request.form['password'])
    return True  
    
@app.route('/h')
def start():  
    return render_template('login.html')


# @app.route('/pruebaArticulos')
# def prueba_articulos():

#     #news = f.filter_by_words("muerto", ws.get_lasextanews() + ws.get_antena3news())
#     news = ws.get_lasextanews() + ws.get_antena3news()
#     data = {
#         'imgs' : [new.get_image() for new in news],
#         'titles' : [new.get_title() for new in news],
#         'urls' : [new.get_url() for new in news]
#     }

#     return render_template('pruebaArticulosFunc.html', data=data)


# Crear una etiqueta {}
# for etiq in ws.get_lasextanews():
#     etiq.get_image()


#Guardar un usuario desde la web a la base, usando el modelo de usuario
@app.route('/save_commonuser', methods=['POST'])
def save_CU():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    new_user = users.commonuser(request.form['username'], hashed_password, request.form['email'], request.form['name'], request.form['lastname'])
    new_G_user = users.user(request.form['username'], hashed_password, request.form['email'])
    db.session.add(new_G_user) 
    db.session.add(new_user)
    db.session.commit()
    
    return "Saving a common user"

@app.route('/save_premiumuser', methods=['POST'])
def save_PU():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    certification = 'certification' in request.form
    new_user = users.premiumuser(request.form['username'], hashed_password, request.form['email'], request.form['name'], request.form['lastname'], request.form['bank_account'], certification)
    new_G_user = users.user(request.form['username'], hashed_password, request.form['email'])
    db.session.add(new_G_user)    
    db.session.add(new_user) 
    db.session.commit()
    
    return "Saving a premium user"

@app.route('/save_journalist', methods=['POST'])
def save_J():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    certification = 'certification' in request.form
    new_user = users.journalist(request.form['username'], hashed_password, request.form['email'], request.form['name'], request.form['lastname'], certification)
    new_G_user = users.user(request.form['username'], hashed_password, request.form['email'])
    db.session.add(new_G_user) 
    db.session.add(new_user) 
    db.session.commit()
    
    return "Saving a journalist"

@app.route('/save_companyuser', methods=['POST'])
def save_CMPU():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    certification = 'certification' in request.form
    new_user = users.companyuser(request.form['username'], hashed_password, request.form['email'], request.form['company_name'], request.form['NIF'], certification)
    new_G_user = users.user(request.form['username'], hashed_password, request.form['email'])
    db.session.add(new_G_user) 
    db.session.add(new_user) 
    db.session.commit()
    
    return "Saving a company user"

#Chequear la conexión a la base de datos
# @app.route('/bd')
# def basicConnection():
#     try:
#         with db.session.begin():
#             result = users.User.query.all()
#             print(result)
#             print('Conexión exitosa!')
#         return "Conexión exitosa!"
#     except Exception as e:
#         print(str(e))
#         return "La conexión falló!"

#MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3307/truthpaper'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

