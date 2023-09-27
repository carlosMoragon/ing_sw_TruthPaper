from flask import Flask, render_template, request, url_for, redirect, jsonify
#from flask_mysqldb import MySQL
from app import app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/base_datos'
db = SQLAlchemy(app) 

#app.config['MYSQL_HOST'] = ''
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'base_datos'
#connection = MySQL(app)


#PENDIENTE: HACER EL TEST Y LA CONEXION
#Flask_mysql manages the opening and closing connection (No need to generate a method, to close it)




