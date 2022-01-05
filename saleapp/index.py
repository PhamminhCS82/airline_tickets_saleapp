from flask import render_template, session, jsonify
from flask_login import login_user
from saleapp import app, utils, login
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
            ad = utils.check_login(user_name=user_name, password=password, role=UserRole.ADMIN)
            employee = utils.check_login(user_name=user_name, password=password, role=UserRole.EMPLOYEE)
            if ad:
                login_user(ad)
                return redirect(url_for(request.args.get('next', 'admin.index')))
            elif employee:
                login_user(employee)
                return redirect(url_for(request.args.get('next', 'index')))
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
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        telephone = request.get('telephone')
        passport = request.get('passport')
        image_path = None
        existed_user = utils.check_existed_user(user_name=user_name)

        try:
            if password.strip().__eq__(confirm_password.strip()):

                if existed_user:
                    error_message = 'Username đã tồn tại!'
                else:
                  image = request.files.get('user-image')
                  if image:
                      response = cloudinary.uploader.upload(image)
                      image_path = response['secure_url']
                  else:
                      image_path = 'https://res.cloudinary.com/dnwauajh9/image/upload/v1641046577/xlq16tk1iswnjeqfv4z4.jpg'
                  utils.add_user(last_name=last_name.strip(),
                                 first_name=first_name.strip(),
                                 user_name=user_name.strip(),
                                 password=password.strip(),
                                 email=email.strip(),
                                 telephone=telephone,
                                 passport=passport,
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


@app.route('/ticket', methods=['get', 'post'])
def book_ticket():
    airports = utils.read_airport()
    error_message = ''

    try:
        if request.method.__eq__('POST'):
            departure = request.form.get('departure')
            destination = request.form.get('destination')
            datetime = request.form.get('datetime')
            seat_class = request.form.get('seat-class')
            if departure.strip().__eq__(destination.strip()):
                error_message = 'Điểm khởi hành không thể trùng với điểm đến'
            else:
                result = utils.search_flight(departure_airport=departure.strip(),
                                                destination_airport=destination.strip(),
                                                flight_datetime=datetime.strip(),
                                                seat_class=seat_class.strip())
                schedules = result[1]
                seat_quantity = result[0]
                print(seat_quantity)
                if schedules:
                    return render_template('ticket.html', airports=airports, schedules=schedules)
                error_message = 'Hiện tại chưa có chuyến bay này!'

    except Exception as ex:
        error_message = 'Hệ thống đã xảy ra lỗi: ' + str(ex)

    return render_template('ticket.html', airports=airports, error_message=error_message )


@app.route('/type-form')
def guest_register():
    error_message = ""
    if request.method.__eq__('POST'):
        last_name = request.form.get('last-name')
        first_name = request.form.get('first-name')
        user_name = request.form.get('user-name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        telephone = request.get('telephone')
        passport = request.get('passport')
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
                               telephone=telephone,
                               passport=passport,
                               image=image_path)
                return redirect(url_for('user_login'))
            else:
                error_message = 'Mật khẩu không trùng nhau!'
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá trình đăng ký!' + str(ex)

    return render_template('register.html', error_message=error_message)


@app.route('/schedule', methods=['get', 'post'])
def schedule():
    airports = utils.read_airport()
    error_message = ""
    if request.method.__eq__('POST'):
        flight_id = request.form.get('flight-id')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        flight_datetime = request.form.get('flight-datetime')
        flight_time = request.form.get('flight-time')

        try:
            utils.add_schedule(flight_id, departure, destination, flight_datetime, flight_time)
            return redirect(url_for('index'))
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá trình đăng ký!' + str(ex)

    return render_template('schedule.html', airports=airports, error_message=error_message)


@app.route('/api/add-to-receipt', methods=['post'])
def add_to_receipt():
    data = request.json
    ticket_id = str(data.get('id'))
    name = str(data.get('name'))
    passport = str(data.get('passport'))
    telephone = str(data.get('telephone'))
    ticket_class = str(data.get('ticket-class'))
    price = str(data.get('price'))
    cart = session.get('cart')
    if not cart:
        cart = {}
    else:
        receipt = {
            'id': ticket_id,
            'name': name,
            'price': price,
            'passport': passport,
            'telephone': telephone,
            'ticket-class': ticket_class
        }
        cart.add(receipt)
        session['cart'] = cart

        return jsonify(session.get('cart'))


@app.route('/api/add-ticket', methods=['post'])
def add_ticket_detail():
    data = request.json
    name = str(data.get('name'))
    passport = str(data.get('passport'))
    telephone = str(data.get('telephone'))
    ticket_class = str(data.get('ticket-class'))
    price = str(data.get('price'))
    cart = session.get('cart')
    if not cart:
        cart = {}
    if passport in cart:
        return jsonify(session.get('cart'))
    else:
        cart[passport] = {
            'name': name,
            'price': price,
            'passport': passport,
            'telephone': telephone,
            'ticket-class': ticket_class
        }
        session['cart'] = cart

        return jsonify(cart[passport])


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/404')
def not_allowed():
    return render_template('404.html')


if __name__ == '__main__':
    from admin import *

    app.run(debug=True)
