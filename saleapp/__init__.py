from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
import stripe


app = Flask(__name__)
app.secret_key = '#$%Y$^HEBberfberblehkjblewb#%$#%$H%11243'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:9875428Minh@localhost/airlinedb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
stripe_keys = {
        "secret_key": 'sk_test_51KE3KdAjNfCIfHPA9zLpbNK75pQk52mO08ddIKaZ0mOEdCZrgQaf2xFKpyBeD5OaqntYSbFKXKbxFDXf0Lf82F3200UtcxcQFE',
        "publishable_key": 'pk_test_51KE3KdAjNfCIfHPA5YsvptWT1TMeS2p1qm2HPq4jK6Gd6kVZy1HG8uU4GGhGrLVx6yIGhULWY2Bc8fciUfxoBZor00Xj5FJuJI',
    }
stripe.api_key = stripe_keys["secret_key"]
# app.config['SQLALCHEMY_RECORDED_QUERIES'] = True

cloudinary.config(
  cloud_name = "dnwauajh9",
  api_key = "897663217318733",
  api_secret = "tXbx6Ne3QD3vpsUt1ryDrZl9OIE"
)

db = SQLAlchemy(app=app)

login = LoginManager(app=app)
