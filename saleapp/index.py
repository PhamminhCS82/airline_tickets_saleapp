import stripe
from flask import render_template, session, jsonify
from flask_login import login_user, login_required
from saleapp import login
import cloudinary.uploader
from saleapp.admin import *


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
    cart = session.get('cart')
    if cart:
        del session['cart']
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


@app.route('/type-form', methods=['get', 'post'])
def guest_register():
    error_message = ""
    if request.method.__eq__('POST'):
        last_name = request.form.get('last-name')
        first_name = request.form.get('first-name')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        passport = request.form.get('passport')
        image_path = None

        try:
            session['guest_user'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'telephone': telephone,
                'passport': passport
            }
            return redirect(url_for('cart'))
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá trình đăng ký!' + str(ex)

    return render_template('guest-form.html', error_message=error_message)


@app.route('/schedule', methods=['get', 'post'])
@login_required
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
            return redirect(url_for('schedule'))
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá trình đăng ký!' + str(ex)

    return render_template('schedule.html', airports=airports, error_message=error_message,
                           all_schedule=utils.get_all_schedule())


@app.route("/schedule-detail-airport")
def schedule_detail_airport():
    flight_id = request.args.get('flight_id')
    return render_template("schedule-detail.html", flight_id=flight_id)


@app.route("/schedule-detail-seat", methods=['get', 'post'])
def schedule_add_seat():
    error_message = ""
    if request.method.__eq__('POST'):
        flight_id = request.form.get('flight-id')
        seat_class = request.form.get('seat_class')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

        try:
            utils.add_seat_schedule(flight_id, price, seat_class, quantity)
            return redirect(url_for('index'))
        except Exception as ex:
            error_message = 'Đã xảy ra lỗi trong quá thêm!' + str(ex)
    return render_template("schedule-seat.html",
                           flight_id=request.args.get('flight_id'),
                           seats=utils.read_seat(),
                           error_message=error_message)


@app.route('/api/add-ticket', methods=['post'])
def add_ticket_detail():
    data = request.json
    ticket_id = str(data.get('ticket_id'))
    name = str(data.get('name'))
    passport = str(data.get('passport'))
    telephone = str(data.get('telephone'))
    ticket_class = str(data.get('ticket_class'))
    price = str(data.get('price'))
    cart = session.get('cart')
    if not cart:
        cart = {}
    if passport in cart:
        return jsonify({'code': 400})
    else:
        cart[passport] = {
            'ticket_id': ticket_id,
            'name': name,
            'price': price,
            'passport': passport,
            'telephone': telephone,
            'ticket_class': ticket_class
        }
        session['cart'] = cart
        return jsonify(cart[passport])


@app.route('/cart')
def cart():
    guest_user = session.get('guest_user')
    if guest_user is not None or current_user.is_authenticated:

        temp_id = session.get('temp')
        if not temp_id:
            temp_id = request.args.get('flight_id')
        flight_id = request.args.get('flight_id')
        if temp_id.__eq__(flight_id) is False:
            session['cart'] = {}
            temp_id = request.args.get('flight_id')
        flight = utils.load_flight(flight_id=flight_id)
        session['temp'] = temp_id
        return render_template('cart.html', flight=flight, cart_stats=utils.cart_stats(session.get('cart')))
    else:
        return render_template('guest-form.html')


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        guest_user = session.get('guest_user')
        if current_user.is_authenticated:
            utils.add_receipt(session.get('cart'), user=current_user)
        elif guest_user is not None:
            guest_user = utils.add_guest(last_name=guest_user['last_name'],
                                         first_name=guest_user['first_name'],
                                         email=guest_user['email'],
                                         telephone=guest_user['telephone'],
                                         passport=guest_user['passport'],
                                         image=None)
            utils.add_receipt(session.get('cart'), user=guest_user)
        else:
            return jsonify({'code': 400})
        del session['cart']
    except Exception as e:
        print(e)
        return jsonify({'code': 404})

    return jsonify({'code': 200})


# Thanh toan online su dung stripe
@app.route('/stripe_pay', methods=['post'])
def create_checkout_session():
    try:
        cart_checkout = utils.cart_stats(session.get('cart'))
        print(cart_checkout)
        session_checkout = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'vnd',
                    'product_data': {
                        'name': 'Ve may bay',
                    },
                    'unit_amount': int(cart_checkout['total_amount']),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cart', _external=True),
        )
        return {
            'checkout_session_id': session_checkout['id'],
            'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
        }
    except Exception as e:
        print(e)
        return jsonify({'code': 400})


@app.route('/thanks')
def thanks():
    # utils.add_receipt(session.get('cart'), user=current_user)
    cart_checkout = session.get('cart')
    cart_stats = utils.cart_stats(session.get('cart'))
    del session['cart']
    print(cart_checkout)
    return render_template('thanks.html', results=cart_checkout, cart_stats=cart_stats)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/history')
@login_required
def history():
    return render_template('history.html', receipts=utils.read_receipt())


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.cart_stats(session.get('cart'))
    }


@app.route('/404')
def not_allowed():
    return render_template('404.html')


if __name__ == '__main__':

    app.run(debug=True)
