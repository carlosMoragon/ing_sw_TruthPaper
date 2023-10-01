from flask import Flask, render_template, request
from modules import web_scrapping as ws, users
from flask_sqlalchemy import SQLAlchemy
from database import DBManager as manager
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
     return 'Hello World!'

@app.route('/pruebaArticulos')
def prueba_articulos():
    news = ws.get_lasextanews() + ws.get_antena3news()
    # all_news = ws.get_lasextanews() + ws.get_antena3news()
    # news = f.filter_by_words("pedro",all_news)
    data = {
        'imgs' : [new.get_image() for new in news],
        'titles' : [new.get_title() for new in news],
        'urls' : [new.get_url() for new in news]
    }

    return render_template('pruebaArticulosFunc.html', data=data)

# Crear una etiqueta {}
for etiq in ws.get_lasextanews():
    etiq.get_image()

#Guardar un usuario desde la web a la base, usando el modelo de usuario
@app.route('/save_user', methods=['POST'])
def save_data():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    new_user = users.User(request.form['user_name'], request.form['email'], hashed_password)
    db.session.add(new_user) 
    db.session.commit()
    
    return "Saving a user"

#Chequear la conexión a la base de datos
@app.route('/bd')
def basicConnection():
    try:
        with db.session.begin():
            result = users.User.query.all()
            print(result)
            print('Conexión exitosa!')
        return "Conexión exitosa!"
    except Exception as e:
        print(str(e))
        return "La conexión falló!"

#MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3307/truthpaperprueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = manager.db
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
