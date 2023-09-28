# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from DBManager import db
# from sqlalchemy import create_engine, MetaData, Table, insert

# app = Flask(__name__)
# data = []

# @app.route('/')
# def hello_world():
#     return 'Hello World!'
    
# @app.route('/bd')
# def basicConnection():
#     try:
#         #with db.engine.connect() as connection:
#             #result = connection.execute("SELECT * from users")
#          #   result = User.query.all()
#             with engine.connect() as connection:
#                 result = connection.execute(insert(user), data)

#             print(result)
#             return "Conexión exitosa!"
#     except Exception as e:
#         print("La conexión falló!")
#         print(str(e))
#         return "La conexión falló!"

# # MySQL Connection
# #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3307/truthpaperprueba'
# #db.init_app(app)
# engine = create_engine('mysql+pymysql://root:1234@localhost:3307/truthpaperprueba')
# metadata = MetaData()

# user = Table('users', metadata, autoload_with=engine)




# if __name__ == "__main__":
#     app.run(debug=True)