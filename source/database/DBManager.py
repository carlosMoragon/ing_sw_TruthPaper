from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# def test_connection():
#     try:
#         with db.engine.connect() as connection:
#             result = connection.execute("SELECT * from users")
#             print(result)
#             print("Conexión exitosa!")
#     except Exception as e:
#         print("La conexión falló!")
#         print(str(e))
    
#db.session to execute querys
#db.Model  to create classes


