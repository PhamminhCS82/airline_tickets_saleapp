from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '#$%Y$^HEBberfberblehkjblewb#%$#%$H%11243'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234567890@localhost/airlinedb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

cloudinary.config(
  cloud_name = "dnwauajh9",
  api_key = "897663217318733",
  api_secret = "tXbx6Ne3QD3vpsUt1ryDrZl9OIE"
)

db = SQLAlchemy(app=app)

login = LoginManager(app=app)
