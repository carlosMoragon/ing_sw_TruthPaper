from flask import Flask
from modules import web_scrapping as ws

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# Crear una etiqueta {}
for etiq in ws.get_lasextanews():
    etiq.get_image()


if __name__ == '__main__':
    app.run()

