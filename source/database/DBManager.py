from flask_sqlalchemy import SQLAlchemy
from modules import users
# from werkzeug.security import generate_password_hash
db = SQLAlchemy()


def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
        return user_db.password == password
    else:
        return False
