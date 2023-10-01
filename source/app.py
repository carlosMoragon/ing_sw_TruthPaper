from flask import Flask, render_template
from modules import web_scrapping as ws

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
     return 'Hello World!'


@app.route('/pruebaArticulos')
def prueba_articulos():
    news = ws.get_lasextanews()
    news = news + ws.get_antena3news()
    data = {
        'imgs' : [new.get_image() for new in news],
        'titles' : [new.get_title() for new in news],
        'urls' : [new.get_url() for new in news]
    }

    return render_template('pruebaArticulosFunc.html', data=data)


# Crear una etiqueta {}
for etiq in ws.get_lasextanews():
    etiq.get_image()


@app.route('/pruebaArticulos')
def prueba_articulos():
    news = ws.get_lasextanews()
    news = news + ws.get_antena3news()
    data = {
        'imgs' : [new.get_image() for new in news],
        'titles' : [new.get_title() for new in news],
        'urls' : [new.get_url() for new in news]
    }

    return render_template('pruebaArticulosFunc.html', data=data)


# Crear una etiqueta {}
for etiq in ws.get_lasextanews():
    etiq.get_image()


if __name__ == '__main__':
    app.run(debug=True)

