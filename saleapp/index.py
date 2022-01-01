from flask import render_template, request, url_for
from flask_login import login_user, logout_user
from saleapp import app, utils, login
from models import UserRole
import cloudinary.uploader


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
    error_message = ""
    if request.method.__eq__('POST'):
        last_name = request.form.get('last-name')
        first_name = request.form.get('first-name')
        user_name = request.form.get('user-name')
        email= request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        image_path = None

        try:
            if password.strip().__eq__(confirm_password.strip()):
                image = request.files.get('user-image')
                if image:
                    response = cloudinary.uploader.upload(image)
                    image_path = response['secure_url']
                utils.add_user(last_name=last_name.strip(),
                               first_name=first_name.strip(),
                               user_name=user_name.strip(),
                               password=password.strip(),
                               email=email.strip(),
                               image=image_path)
                return redirect(url_for('user_login'))
            else:
                error_message = 'Mật khẩu không trùng nhau!'
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá trình đăng ký!' + str(ex)

    return render_template('register.html', error_message=error_message)


@app.route('/about')
def contact_us():
    return render_template('contact.html')


@app.route('/ticket')
def book_ticket():
    return render_template('ticket.html')


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)
