from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '#$%Y$^HEBberfberblehkjblewb#%$#%$H%11243'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:9875428Minh@localhost/airlinedb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)