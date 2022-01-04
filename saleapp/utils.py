import hashlib
from models import User, UserRole, Airport, FlightSchedule, Receipt, TicketDetail
from saleapp import db
from flask_login import current_user


def check_login(user_name, password, role=UserRole.USER):
    if user_name and password:
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

        return User.query.filter(User.user_name.__eq__(user_name.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    if user_id:
        return User.query.get(user_id)


def check_existed_user(user_name):
    if user_name:
        return User.query.filter(User.user_name.__eq__(user_name.strip))


def add_user(last_name, first_name, user_name, password, email, telephone, passport, image):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    new_user = User(last_name=last_name.strip(),
                    first_name=first_name.strip(),
                    user_name=user_name.strip(),
                    password=password,
                    email=email.strip(),
                    phone_number=telephone,
                    passport=passport,
                    image=image)
    db.session.add(new_user)
    db.session.commit()


def add_guest(last_name, first_name, email, telephone, passport, image):
    new_user = User(last_name=last_name.strip(),
                    first_name=first_name.strip(),
                    email=email.strip(),
                    phone_number=telephone,
                    passport=passport,
                    image=image)
    db.session.add(new_user)
    db.session.commit()


def read_airport():
    return Airport.query.all()


def add_schedule(id, departure, destination, flight_datetime, flight_time):
    new_schedule = FlightSchedule(id=id, departure_airport=departure,
                                  destination_airport=destination,
                                  flight_datetime=flight_datetime,
                                  flight_time=flight_time)
    db.session.add(new_schedule)
    db.session.commit()


def get_all_schedule():
    return FlightSchedule.query.all()


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user, quantity=len(cart))
        db.session.add(receipt)

        for c in cart.values():
            d = TicketDetail(receipt=receipt,
                             ticket_id=c['ticket_id'],
                             user_name=c['name'],
                             passport=c['passport'],
                             telephone=c['telephone'],
                             ticket_class=c['ticket_class'],
                             price=c['price']
                             )
            db.session.add(d)

        db.session.commit()


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        total_quantity = len(cart)
        for c in cart.values():
            total_amount += float(c['price'])

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }



def load_flight(flight_id):
    return FlightSchedule.query.filter(FlightSchedule.id.__eq__(flight_id)).first()