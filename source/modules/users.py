from database import DBManager as manager
db = manager.db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=True)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Userclient(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    is_checked = db.Column(db.Enum('Y', 'N'), nullable=False)
    
    def __init__(self, client_id, photo, is_checked):
        self.client_id = client_id
        self.photo = photo
        self.is_checked = is_checked   


class Commonuser(db.Model):
    commonuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)
    
    def __init__(self, commonuser_id, name, lastname, bankaccount):
        self.commonuser_id = commonuser_id
        self.name = name
        self.lastname = lastname
        self.bankaccount = bankaccount


class Companyuser(db.Model):
    companyuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    NIF = db.Column(db.Integer, nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)
    
    def __init__(self, companyuser_id, name, NIF, bankaccount):
        self.companyuser_id = companyuser_id
        self.name = name

        self.NIF = NIF
        self.bankaccount = bankaccount


class Journalistuser(db.Model):
    journalistuser_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    certificate = db.Column(db.LargeBinary, nullable=True)
    
    def __init__(self, journalistuser_id, name, lastname, certificate):
        self.journalistuser_id = journalistuser_id
        self.name = name
        self.lastname = lastname
        self.certificate = certificate    


class AdministratorUser(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    can_create = db.Column(db.Boolean, nullable=False, default=True)
    can_delete = db.Column(db.Boolean, nullable=False, default=True)
    can_edit = db.Column(db.Boolean, nullable=False, default=True)

    def _init_(self, admin_id, can_create, can_delete, can_edit):
        self.admin_id = admin_id
        self.can_create = can_create
        self.can_delete = can_delete    
        self.can_edit = can_edit    


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    owner = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    container = db.Column(db.Integer, nullable=False)
    journalistuser_id = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    views = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id, owner, title, image, url, content, container, journalistuser_id, date, category, likes, views):
        self.id = id
        self.owner = owner
        self.title = title
        self.image = image
        self.url = url
        self.content = content
        self.container = container
        self.journalistuser_id = journalistuser_id
        self.date = date
        self.category = category
        self.likes = likes
        self.views = views


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Integer, nullable=True, default=0)
    views = db.Column(db.Integer, nullable=True, default=0)
    content = db.Column(db.Text, nullable=True)
    image = db.Column(db.BLOB, nullable=True)
    userclient_id = db.Column(db.Integer, db.ForeignKey('userclient.client_id'), nullable=True)
    idNew = db.Column(db.Integer, db.ForeignKey('new.id'), nullable=True)

    def __init__(self, likes, views, content, image, userclient_id, idNew):
        self.likes = likes
        self.views = views
        self.content = content
        self.image = image
        self.userclient_id = userclient_id
        self.idNew = idNew


