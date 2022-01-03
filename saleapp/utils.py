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
        receipt = Receipt(user=current_user)
        ticket = db.session.get('ticket')
        db.session.add(receipt)

        for c in cart.values():
            d = TicketDetail(receipt=receipt,
                             ticket=ticket,
                             user_name=c['name'],
                             passport=c['passport'],
                             telephone=c['telephone'],
                             ticket_class=c['ticket-class'],
                             price=c['price']
                             )
            db.session.add(d)

        db.session.commit()