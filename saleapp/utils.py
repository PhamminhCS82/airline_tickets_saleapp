import hashlib

from sqlalchemy import func, extract, or_

from saleapp.models import User, UserRole, Airport, FlightSchedule, Receipt, TicketDetail, Ticket
from saleapp import db


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
                    user_role=UserRole.GUEST,
                    image=image)
    db.session.add(new_user)
    db.session.commit()
    return new_user


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


def add_receipt(cart, user):
    if cart:
        receipt = Receipt(user=user, quantity=len(cart))
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


def flight_stats(kw=None, from_date=None, to_date=None):
    f = db.session.query(func.concat(FlightSchedule.departure_airport, ' - ', FlightSchedule.destination_airport),
                         func.sum(TicketDetail.price)) \
        .join(Ticket, Ticket.flight_id.__eq__(FlightSchedule.id))\
        .join(TicketDetail, TicketDetail.ticket_id.__eq__(Ticket.id))\
        .group_by(FlightSchedule.departure_airport, FlightSchedule.destination_airport)

    if kw:
        f = f.filter(or_(FlightSchedule.departure_airport.contains(kw), FlightSchedule.destination_airport.contains(kw)))

    if from_date:
        f = f.filter(FlightSchedule.flight_datetime.__ge__(from_date))

    if to_date:
        f = f.filter(FlightSchedule.flight_datetime.__le__(to_date))

    return f.all()


def flight_count():
    f = db.session.query(func.concat(FlightSchedule.departure_airport, ' - ', FlightSchedule.destination_airport),
                         func.count(FlightSchedule.id))\
        .group_by(FlightSchedule.departure_airport, FlightSchedule.destination_airport)
    return f.all()


def flight_month_stats(year):
    return db.session.query(extract('month', FlightSchedule.flight_datetime),
                            func.sum(TicketDetail.price)) \
            .join(Ticket, Ticket.flight_id.__eq__(FlightSchedule.id)) \
            .join(TicketDetail, TicketDetail.ticket_id.__eq__(Ticket.id))\
            .filter(extract('year', FlightSchedule.flight_datetime) == year)\
            .group_by(extract('month', FlightSchedule.flight_datetime))\
            .order_by(extract('month', FlightSchedule.flight_datetime)).all()