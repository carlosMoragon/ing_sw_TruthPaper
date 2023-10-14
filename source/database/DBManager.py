from flask_sqlalchemy import SQLAlchemy
from modules import users, classes as cl
db = SQLAlchemy()


def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
        return user
        db.password == password
    else:
        return False


# CONSULTA A LA BBDD PARA QUE TE COJA LAS NOTICIAS -> SE VA A LLAMAR A ESTA FUNCION DESDE APP.PY ANTES DE INICIAR
"""
def get_news_db() -> List[cl.News]:
    return None
"""