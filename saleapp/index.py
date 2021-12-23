from flask import render_template, request, url_for
from flask_login import login_user, logout_user
from saleapp import app, utils, login
from models import UserRole


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['get', 'post'])
def user_login():
    error_message = ''
    if request.method.__eq__('POST'):
        user_name = request.form.get('user-name')
        password = request.form.get('password')
        user = utils.check_login(user_name=user_name, password=password)

        if user:
            login_user(user)
            return redirect(url_for(request.args.get('next', 'index')))
        else:
            admin = utils.check_login(user_name=user_name, password=password, role=UserRole.ADMIN)
            if admin:
                login_user(admin)
                return redirect(url_for(request.args.get('next', 'admin.index')))
            error_message = 'Tài khoản hoặc mật khẩu không đúng'
    return render_template('login.html', error_message=error_message)


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['get', 'post'])
def user_register():
    return render_template('register.html')


@app.route('/about')
def contact_us():
    return render_template('contact.html')


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)
