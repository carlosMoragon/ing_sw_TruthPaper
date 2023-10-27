from flask import Flask

# DB Manager
from .database import DBManager

# Routes
from .routes import routes

app = Flask(__name__, template_folder='../web_rsrc/templates')


# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://administrador_truthpaper:Periodico55deVerdad@truthpaper-server.mysql.database.azure.com:3306/truthpaper_ddbb?charset=utf8mb4&ssl_ca=DigiCertGlobalRootCA.crt.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(routes.main, url_prefix='/')

    db = DBManager.db
    db.init_app(app)

    return app
