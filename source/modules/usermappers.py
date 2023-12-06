from database.DBManager import db 
from flask_bcrypt import Bcrypt
from flask import request
from io import BytesIO
from PIL import Image
import base64
import re 

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Enum('N', 'Y'), nullable=False, default='N')

    def __init__(self, username, password, email, verified):
        self.username = username
        self.password = password
        self.email = email
        self.verified = verified
    
    def get_user_email(id):
        return User.query.filter_by(id=id).first().email

    def get_user_verified(id):
        return User.query.filter_by(id=id).first().verified

    def getAllUserData(username): #maybe debería ser id 
        return User.query.filter_by(username=username).first()

    def find_user_by_username_or_email(username_or_email):
        user_db = User.query.filter_by(username=username_or_email).first()
        if user_db is None:
            user_db = User.query.filter_by(email=username_or_email).first()
        return user_db

    def get_all_users_username_and_email():
        users = User.query.all()
        users_username = [user.username for user in users]
        users_email = [user.email for user in users]
        return users_username, users_email
    
    def login(username, password): #-> bool:
        user_db =  User.find_user_by_username_or_email(username)
        if user_db == None:
            return False
      
        encoded_password = password.encode('utf-8')
        if bcrypt.check_password_hash(user_db.password, encoded_password):
            if user_db.verified == 'Y':
                admin_id = AdministratorUser.adminUsersIds()
                if (user_db.id in admin_id):
                    return 'admin'
            
                return True
            else:
                return False
        else:
            return False

    def save_user():
        if validate_password(request.form['password']):
            if validate_email(request.form['email']):
                if validate_not_duplicates(request.form['username'], request.form['email']):
                    newUser =  User(
                        username=request.form['username'],
                        password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
                        email=request.form['email'],
                        verified='N')

                    db.session.add(newUser)
                    db.session.commit()

                    new_user_id = newUser.id
                    newUserClient =  Userclient(
                        client_id=new_user_id,
                        is_checked='Y',
                        photo=request.files['photo'].read()
                    )
                    db.session.add(newUserClient)
                    db.session.commit()

                    return new_user_id
                else: 
                    print("NOMBRE DE USUARIO O EMAIL DUPLICADO")
                    return -3
            else:
                print("EMAIL NO VÁLIDO")
                return -2
        else:
            print("CONTRASEÑA DÉBIL")
            return -1


class AdministratorUser(db.Model):
    __tablename__ = 'administratoruser'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    can_create = db.Column(db.Enum('N', 'Y'), nullable=False, default='Y')
    can_delete = db.Column(db.Enum('N', 'Y'), nullable=False, default='Y')
    can_edit = db.Column(db.Enum('N', 'Y'), nullable=False, default='Y')
    
    def __init__(self, admin_id, can_create, can_delete, can_edit):
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
            can_create='Y',
            can_delete='Y',
            can_edit='Y'
            )
        db.session.add(newAdminUser)
        db.session.commit()
        return True
        

class Userclient(db.Model):
    __tablename__ = 'userclient'
    extend_existing=True
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    is_checked = db.Column(db.Enum('Y', 'N'), nullable=False)

    def __init__(self, client_id, photo, is_checked):
        self.client_id = client_id
        self.photo = photo
        self.is_checked = is_checked

    def load_image(user_id):
        user =  Userclient.query.filter_by(client_id=user_id).first()
        if user and user.photo:
            image_bytes = user.photo
            base64_image = transform_images_to_base64(image_bytes)
            return base64_image
        else:
            return None

    def loadUncheckedUsers():
        uncheckedUserList = []
        for user in  Userclient.query.all():
            if user.is_checked == 'N':
                usuario = User.query.filter_by(id=user.client_id).first()
                uncheckedUserList.append([usuario.username, usuario.password, usuario.email, user.client_id])
        return uncheckedUserList

    def updateUserChecked(id):
        user =  Userclient.query.filter_by(client_id=id).first()
        user.is_checked = 'Y'
        db.session.commit()




class Commonuser(db.Model):
    __tablename__ = 'commonuser'
    commonuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)

    def __init__(self, commonuser_id, name, lastname, bankaccount):
        self.commonuser_id = commonuser_id
        self.name = name
        self.lastname = lastname
        self.bankaccount = bankaccount
    
    def save_commonuser(new_user_id) -> bool:
        newCommonUser =  Commonuser(
            commonuser_id = new_user_id, 
            name = request.form['c_user_name'],
            lastname = request.form['c_user_lastname'],
            bankaccount = request.form['bankaccount']
        )
        db.session.add(newCommonUser)
        db.session.commit()
        return True
            
            
class Companyuser(db.Model):
    __tablename__ = 'companyuser'
    companyuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    NIF = db.Column(db.Integer, nullable=False)
    bankaccount = db.Column(db.String(70), nullable=False)

    def __init__(self, companyuser_id, name, NIF, bankaccount):
        self.companyuser_id = companyuser_id
        self.name = name

        self.NIF = NIF
        self.bankaccount = bankaccount
    
    def save_companyuser(new_user_id) -> bool:
        newCompanyUser =  Companyuser(
                companyuser_id = new_user_id, 
                name = request.form['company_name'],
                bankaccount = request.form['bankaccount'],
                NIF = request.form['company_nif']
            )
        db.session.add(newCompanyUser)
        db.session.commit()
        return True


class Journalistuser(db.Model):
    __tablename__ = 'journalistuser'
    journalistuser_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    certificate = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, journalistuser_id, name, lastname, certificate):
        self.journalistuser_id = journalistuser_id
        self.name = name
        self.lastname = lastname
        self.certificate = certificate
    
    def save_journalistuser(new_user_id) -> bool:
        newJournalistUser =  Journalistuser(
                journalistuser_id = new_user_id, 
                name = request.form['journalist_name'],
                lastname = request.form['journalist_lastname'],
                certificate = request.files['certificate'].read()
            )
        db.session.add(newJournalistUser)
        db.session.commit()
        return True
    
    def load_pdf_certificate(user_id):
        journalistuser =  Journalistuser.query.filter_by(journalistuser_id=user_id).first()
        certificate_bytes = journalistuser.certificate 
        certificate_base64 = base64.b64encode(certificate_bytes).decode('utf-8')
        return certificate_base64



def validate_password(password: str) -> bool:
    # Busca que tenga al menos 4 numeros, 1 mayuscula, 1 caracter especial y 8 digitos
    return bool(re.match(r'^(?=.*\d{4,})(?=.*[A-Z])(?=.*[\W_]).{8,}$', password))

def validate_email(email: str) -> bool:
    # Busca una expresión del tipo (string1)@(string2).(2+characters)
    return bool(re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))

def validate_not_duplicates(username, email) -> bool:
    lista_de_users, lista_de_email = User.get_all_users_username_and_email()
    if (username in lista_de_users) or (email in lista_de_email):
        return False
    else:
        return True
    
    
#Lo podemos dejar en el manager, pero estoy probando otras cosas antes 
def transform_images_to_base64(photo_bytes):
    pil_image = Image.open(BytesIO(photo_bytes))
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    base64_image = base64.b64encode(photo_bytes).decode('utf-8')
    return base64_image