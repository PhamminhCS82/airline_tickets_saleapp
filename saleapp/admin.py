from saleapp import app
from flask_admin.contrib.sqla import ModelView
from saleapp import db
from models import User, UserRole
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask import redirect, request, url_for
from flask_login import logout_user, current_user


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role.__eq__(UserRole.ADMIN)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return super(MyAdminIndexView, self).index()
        next_url = request.endpoint
        login_url = '%s?next=%s' % (url_for('admin_login'), next_url)
        return redirect(login_url)


admin = Admin(app=app,
              name="Administrator",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView(name='Home', menu_icon_type='fa', menu_icon_value='fa-home'))


admin.add_view(AuthenticatedView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(LogoutView(name='Signout', menu_icon_type='fa', menu_icon_value='fa-sign-out'))
