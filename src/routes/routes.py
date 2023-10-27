from flask import Blueprint, render_template, request
from src.services import filter as f, threading as thr
from src.database import DBManager


main = Blueprint('main_blueprint', __name__)


@main.route('index')
def index():
    news_list = thr.get_news()
    containers_list = thr.get_containers()
    thr.init_news.join()
    data = {
        'imgs': [new.get_image() for new in news_list],
        'titles': [str(new.get_title()) for new in news_list],
        'urls': [new.get_url() for new in news_list],
        'dates': [new.get_date() for new in news_list],
        'categories': [new.get_category() for new in news_list]
    }

    return render_template('indexFunc.html', data=data, containers=containers_list)


# Método para ver un contenedor específico
@main.route('ver_contenedor/<int:idn>')
def expand_container(idn):
    container = thr.get_containers().get(idn)
    return render_template('containerNews.html', container=container)


@main.route('/')
def start():
    thr.init_thread()
    return render_template('login.html')


# CAMBIAR LA RUTA
@main.route('login_users', methods=['POST'])
def login_users():
    if DBManager.login(request.form['username'], request.form['password']):
        return index()
    else:
        return render_template('fail_login.html')


@main.route('register.html')
def register_funct():
    return render_template('register.html')


@main.route('login_back')
def go_to_login():
    return render_template('login.html')


@main.route('login_back')
def go_to_profile():
    return render_template('perfil.html')


@main.route('termsandConditions')
def terms_conditions():
    return render_template('termsConditions.html')


@main.route('categories')
def go_to_categories():
    return render_template('categories.html')


@main.route('save_keyword', methods=['POST'])
def save_keyword():
    keyword = request.form['search']
    news_list = thr.get_news()
    filted_news = f.filter_by_words(keyword, news_list)
    data = {
        'imgs': [new.get_image() for new in filted_news],
        'titles': [new.get_title() for new in filted_news],
        'urls': [new.get_url() for new in filted_news],
        'keyword': keyword,
        'dates': [new.get_date() for new in filted_news],
        'categories': [new.get_category() for new in filted_news]
    }
    return render_template('categoriesFunc.html', data=data)


# @main.route('pruebaArticulos')
# def prueba_articulos():
#     global news
#     # news = ws.get_news()
#     data = {
#         'imgs' : [new.get_image() for new in news],
#         'titles' : [new.get_title() for new in news],
#         'urls' : [new.get_url() for new in news]
#     }
#     return render_template('pruebaArticulos.html', data=data)

# Aun en PROCESO se MEJORA y DEPURACIÓN

@main.route('save_commonuser', methods=['POST'])
def register_user():
    result = DBManager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if DBManager.save_journalist_user(result):
            return index()


@main.route('save_companyUser', methods=['POST'])
def register_company_user():
    result = DBManager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if DBManager.save_journalist_user(result):
            return index()


@main.route('save_journalistUser', methods=['POST'])
def register_journalist_user():
    result = DBManager.save_user()
    if result == -1:
        return render_template('fail_register_password.html')
    elif result == -2:
        return render_template('fail_register_email.html')
    else:
        if DBManager.save_journalist_user(result):
            return index()


# Métodos para el ADMINISTRADOR
@main.route('userAdmin.html')
def index_admin():
    # noticias = ws.get_news()
    # gr.graph_news_per_source(noticias)
    return render_template('userAdmin/indexAdmin.html')


@main.route('verifyUsers')
def verify_users():
    unchecked_users = DBManager.load_unchecked_users()
    return render_template('userAdmin/verifyUsers.html', unchecked_users=unchecked_users)


# Método para verificar a los usuarios (Y: cambiar el estado de is_checked a 'Y')
@main.route('process_verification', methods=['POST'])
def process_verification():
    user_id = request.form.get('user_id')
    action = request.form.get('action')  # 'accept' or 'reject'
    if action == 'accept':
        DBManager.update_user_checked(user_id)
    return render_template('userAdmin/verifyUsers.html')


@main.route('charts')
def charts():
    return render_template('userAdmin/charts.html')


@main.route('comments')
def comments():
    return render_template('userAdmin/comments.html')


@main.route('editUsers')
def edit_users():
    return render_template('userAdmin/editUsers.html')


@main.route('profileAdmin')
def profile_admin():
    return render_template('userAdmin/profileAdmin.html')


@main.route('pdfreader')
def pdf_reader():
    return render_template('userAdmin/pdfReader.html')
