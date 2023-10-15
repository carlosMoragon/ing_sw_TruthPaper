from flask_sqlalchemy import SQLAlchemy
from modules import users, classes as cl
db = SQLAlchemy()
from flask import request

def login(username, password) -> bool:
    user_db = users.User.query.filter_by(username=username).first()
    if user_db:
        return user
        db.password == password
    else:
        return False


def type_of_user():
    return True 

def save_commonuser() -> bool:
    if cl.validate_password(request.form['password']):
       #Si el nombre de usuario ya existe, no se puede registrar
        newUser = users.User(
            username=request.form['username'], 
            password=request.form['password'], 
            email=request.form['email'])
        
        db.session.add(newUser)
        db.session.commit()

        # Obtiene el ID del nuevo usuario
        new_user_id = newUser.id
        newUserClient = users.Userclient(
            client_id=new_user_id,
            is_checked=True,
            photo=None  
        )
        db.session.add(newUserClient)
        db.session.commit()

        newCommonUser = users.Commonuser(
            commonuser_id=new_user_id, 
            name=request.form['c_user_name'],
            lastname=request.form['c_user_lastname'],
            bankaccount=request.form['bankaccount']
        )
        db.session.add(newCommonUser)
        db.session.commit()

        return True
    else:
        print("CONTRASEÑA DÉBIL")
        #flash('CONTRASEÑA DÉBIL', 'WARNING')
        return False
   
def save_cmpu():
    if cl.validate_password(request.form['password']):
        newUser = users.User(
                username=request.form['username'], 
                password=request.form['password'], 
                email=request.form['email'])
            
        db.session.add(newUser)
        db.session.commit()

        new_user_id = newUser.id
        newUserClient = users.Userclient(
                client_id=new_user_id,
                is_checked=True,
                photo=None  
            )
        db.session.add(newUserClient)
        db.session.commit()

        newCompanyUser = users.Commonuser(
                commonuser_id=new_user_id, 
                name=request.form['c_user_name'],
                NIF=request.form['NIF'],
                bankaccount=request.form['bankaccount']
            )
        db.session.add(newCompanyUser)
        db.session.commit()

        return True

    else:
      print("CONTRASEÑA DÉBIL")
      #flash('CONTRASEÑA DÉBIL', 'WARNING')
      return False