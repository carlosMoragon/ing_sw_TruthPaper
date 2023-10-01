# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, request
# from DBManager import db
# from modules.users import User


# app = Flask(__name__)
# db.init_app(app)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'
    
    
# #Guardar un usuario desde la web a la base, usando el modelo de usuario
# @app.route('/save_data', methods=['POST'])
# def save_data():
#     new_user = User(request.form['user_name'], request.form['email'], request.form['password'])
#     db.session.add(new_user) 
#     db.session.commit()
    
#     return "Saving a user"


# @app.route('/bd')
# def basicConnection():
#     try:
#             with app.connect() as connection:
#                 result = User.query.all()
#             print(result)
#             return "Conexión exitosa!"
#     except Exception as e:
#         print("La conexión falló!")
#         print(str(e))
#         return "La conexión falló!"

# #MySQL Connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3307/truthpaperprueba'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# if __name__ == "__main__":
#     app.run(debug=True)