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
            return redirect(url_for('index'))
        else:
            error_message = 'Tên đăng nhập hoặc mật khẩu không hợp lệ'

    return render_template('login.html', error_message=error_message)


@app.route('/adminLogin', methods=['post', 'get'])
def admin_login():
    if request.method.__eq__('POST'):
        user_name = request.form.get('user-name')
        password = request.form.get('password')
        user = utils.check_login(user_name=user_name, password=password, role=UserRole.ADMIN)

        if user:
            login_user(user)
            destination = request.args.get('next')
            fallback = url_for('admin.index')
            try:
                destination_url = url_for(destination)
                return redirect(destination_url)
            except:
                return  redirect(fallback)
    return render_template('admin-login.html')


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


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)
