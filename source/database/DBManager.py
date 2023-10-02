from flask_sqlalchemy import SQLAlchemy
from modules import users
#from werkzeug.security import generate_password_hash
db = SQLAlchemy()

def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
        #if generate_password_hash(user_db.password, password):
        if (user_db.password, password):
            return 'Yeii'
        else:
            return 'Nope'
    else:
        return 'No estas registrado'
 




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
