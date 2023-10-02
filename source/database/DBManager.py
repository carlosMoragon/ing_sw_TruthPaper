from flask_sqlalchemy import SQLAlchemy
from modules.users import commonuser
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

def login(username, password) -> bool:
    user = user.query.filter_by(username=username).first()
    if user:
        if generate_password_hash(user.password, password):
            return True
        else:
            return False
    else:
        return True
 

