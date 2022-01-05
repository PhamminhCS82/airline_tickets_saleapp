from saleapp import app, utils
from flask_admin.contrib.sqla import ModelView
from saleapp import db
from saleapp.models import UserRole, User, FlightSchedule, Airport, IntermediateAirport, SeatClass, Ticket
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask import redirect, request, url_for
from flask_login import logout_user, current_user
from datetime import datetime


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
            return super(MyAdminIndexView, self).index()
        next_url = request.endpoint
        login_url = '%s?next=%s' % (url_for('user_login'), next_url)
        return redirect(login_url)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',
                           flight_amount_stats=utils.flight_stats(kw,from_date,to_date),
                           flight_count=utils.flight_count(),
                           month_stats=utils.flight_month_stats(year=year))

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN


admin = Admin(app=app,
              name="Administrator",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView(name='Home', menu_icon_type='fa', menu_icon_value='fa-home'))


admin.add_view(AuthenticatedView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(AuthenticatedView(FlightSchedule, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(AuthenticatedView(SeatClass, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(AuthenticatedView(Ticket, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(AuthenticatedView(IntermediateAirport, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(AuthenticatedView(Airport, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(StatsView(name='Stats', menu_icon_type='fa',menu_icon_value='fa-user'))
admin.add_view(LogoutView(name='Signout', menu_icon_type='fa', menu_icon_value='fa-sign-out'))