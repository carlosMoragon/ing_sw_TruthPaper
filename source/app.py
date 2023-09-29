from flask import Flask
from modules import classes as cl, webScrapping as ws

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    # get_news()
    # app.run()
    carlos = cl.CommonUser("carlosXD", "1234", "carlos@gmail.com", "Carlos", "123456789", [], True)
    print("a")
