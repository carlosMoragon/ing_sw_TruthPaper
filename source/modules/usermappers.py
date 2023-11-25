from database.DBManager import db 
from flask_bcrypt import Bcrypt
import re 
from flask import request

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=True)

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def getAllUserData(username): #maybe debería ser id 
        return User.query.filter_by(username=username).first()

    def find_user_by_username_or_email(username_or_email):
        user_db = User.query.filter_by(username=username_or_email).first()
        if user_db is None:
            user_db = User.query.filter_by(email=username_or_email).first()
        return user_db

    def login(username, password): #-> bool:
        user_db =  User.find_user_by_username_or_email(username)
        if user_db == None:
            return False

        admin_id = AdministratorUser.adminUsersIds()
        if (user_db.id in admin_id):
            return 'admin'
        
        encoded_password = password.encode('utf-8')
        if bcrypt.check_password_hash(user_db.password, encoded_password):
            return True
        else:
            return False

    # def save_user():
    #     if validate_password(request.form['password']):
    #         if validate_email(request.form['email']):
    #             #Si el nombre de usuario ya existe, no se puede registrar
    #             newUser =  User(
    #                 username=request.form['username'],
    #                 password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
    #                 email=request.form['email'])

    #             db.session.add(newUser)
    #             db.session.commit()

    #             new_user_id = newUser.id
    def save_user():
        newUser =  User(
            username='usuarioAdministrador',
            password=bcrypt.generate_password_hash('Contraseña1234*').decode('utf-8'),
            email='admin@mail.com')

        db.session.add(newUser)
        db.session.commit()

        new_user_id = newUser.id
        #         newUserClient =  Userclient(
        #             client_id=new_user_id,
        #             is_checked='Y',
        #             photo=request.files['photo'].read()
        #             # photo = transform_images_to_jpeg(request.files['photo'].read())
        #         )
        #         db.session.add(newUserClient)
        #         db.session.commit()

        return new_user_id
        #     else:
        #         print("EMAIL NO VÁLIDO")
        #         return -2
        # else:
        #     print("CONTRASEÑA DÉBIL")
        #     return -1


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
        
    def adminUsersIds():
        admin_ids = [admin.admin_id for admin in AdministratorUser.query.all()]
        return admin_ids
    
    def saveUserAdmin(new_user_id) -> bool:
        newAdminUser =  AdministratorUser(
            admin_id=new_user_id,
            can_create=True,
            can_delete=True,
            can_edit=True)
        db.session.add(newAdminUser)
        db.session.commit()
        return True
        


# class Userclient(db.Model):
#     client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     photo = db.Column(db.LargeBinary, nullable=True)
#     is_checked = db.Column(db.Enum('Y', 'N'), nullable=False)

#     def __init__(self, client_id, photo, is_checked):
#         self.client_id = client_id
#         self.photo = photo
#         self.is_checked = is_checked


# class Commonuser(db.Model):
#     commonuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), nullable=False)
#     lastname = db.Column(db.String(30), nullable=False)
#     bankaccount = db.Column(db.String(70), nullable=False)

#     def __init__(self, commonuser_id, name, lastname, bankaccount):
#         self.commonuser_id = commonuser_id
#         self.name = name
#         self.lastname = lastname
#         self.bankaccount = bankaccount


# class Companyuser(db.Model):
#     companyuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), nullable=False)
#     NIF = db.Column(db.Integer, nullable=False)
#     bankaccount = db.Column(db.String(70), nullable=False)

#     def __init__(self, companyuser_id, name, NIF, bankaccount):
#         self.companyuser_id = companyuser_id
#         self.name = name

#         self.NIF = NIF
#         self.bankaccount = bankaccount


# class Journalistuser(db.Model):
#     journalistuser_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
#     name = db.Column(db.String(50), nullable=False)
#     lastname = db.Column(db.String(50), nullable=False)
#     certificate = db.Column(db.LargeBinary, nullable=True)

#     def __init__(self, journalistuser_id, name, lastname, certificate):
#         self.journalistuser_id = journalistuser_id
#         self.name = name
#         self.lastname = lastname
#         self.certificate = certificate



def validate_password(password: str) -> bool:
    # Busca que tenga al menos 4 numeros, 1 mayuscula, 1 caracter especial y 8 digitos
    return bool(re.match(r'^(?=.*\d{4,})(?=.*[A-Z])(?=.*[\W_]).{8,}$', password))


def validate_email(email: str) -> bool:
    # Busca una expresión del tipo (string1)@(string2).(2+characters)
    return bool(re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))
