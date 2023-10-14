import database.DBManager as manager
#import users, classes as cl
from modules.users import User
db = manager.db

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=True)
    can_delete = db.Column(db.Boolean, nullable=False)
    can_edit = db.Column(db.Boolean, nullable=False)
    can_create = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, username, password, email, can_delete, can_edit, can_create):
        self.username = username
        self.password = password
        self.email = email
        self.can_delete = can_delete
        self.can_edit = can_edit
        self.can_create = can_create


    def loadUncheckedUsers():
        uncheckedUsers = users.User.query.filter_by(is_checked= False).all()
        usersUnchecked = {}
        for user in uncheckedUsers:
            usersUnchecked[user.id] = [user.username, user.password, user.email, user.is_checked]


