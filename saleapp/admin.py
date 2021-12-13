from saleapp import app
from flask_admin.contrib.sqla import ModelView
from saleapp import db
from models import User, UserRole
from flask_admin import Admin
from flask_admin import BaseView, expose
from flask import redirect
from flask_login import logout_user, current_user


admin = Admin(app=app,
              name="Administrator",
              template_mode='bootstrap4')


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AuthenticatedView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
