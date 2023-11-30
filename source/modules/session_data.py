from modules import classes as cl
from flask import session
import uuid

def s_login(user_id):
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    session['user_id'] = user_id
    return user_id

def logout(session_id):
    session.pop(session_id, None)

def get_id():
    return session['user_id']

#def get_session_id():
#    return session['id']