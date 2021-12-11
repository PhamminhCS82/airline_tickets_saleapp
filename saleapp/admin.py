from saleapp import app
from flask_admin.contrib.sqla import ModelView
from saleapp import db
from saleapp.models import User
from flask_admin import Admin


admin = Admin(app=app, name="Administrator", template_mode='bootstrap4')

admin.add_view(ModelView(User, db.session))