import hashlib
from saleapp import db
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    EMPLOYEE = 3
    GUEST = 4


class User(BaseModel, UserMixin):
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=True, unique=True)
    password = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    create_date = Column(DateTime, default=datetime.now())
    phone_number = Column(Integer, nullable=False)
    passport = Column(Integer, unique=True, nullable=False)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    receipts = relationship('Receipt', backref='user', lazy=True)

    def has_roles(self):
        return UserRole.EMPLOYEE.__eq__(self.user_role)


class Airport(db.Model):
    __tablename__ = 'airport'

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False, unique=True)
    airport = relationship('IntermediateAirport', backref='airport', lazy=True)

    def __str__(self):
        return self.name


class FlightSchedule(db.Model):
    __tablename__ = 'flight_schedule'

    id = Column(String(20), primary_key=True, nullable=False)
    departure_airport = Column(String(10), ForeignKey(Airport.id), nullable=False)
    destination_airport = Column(String(10), ForeignKey(Airport.id), nullable=False)
    flight_datetime = Column(DateTime, nullable=False)
    flight_time = Column(Float, nullable=False)
    option = relationship('IntermediateAirport', backref='flight_schedule', lazy=True)
    seat_class = relationship('Ticket', backref='flight_schedule', lazy=True)


class SeatClass(BaseModel):
    __tablename__ = 'seat_class'

    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    seat_class = relationship('Ticket', backref='seat_class', lazy=True)


class Ticket(BaseModel):
    __tablename__ = 'ticket'

    seat_class_id = Column(Integer, ForeignKey(SeatClass.id), primary_key=True)
    flight_id = Column(String(20), ForeignKey(FlightSchedule.id), primary_key=True)
    seat_quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, default=0)
    ticket_class = relationship(SeatClass, backref='ticket', lazy=True)
    ticket_details = relationship('TicketDetail', backref='ticket', lazy=True)


class IntermediateAirport(db.Model):
    __tablename__ = 'intermediate_airport'

    airport_id = Column(String(10), ForeignKey(Airport.id), primary_key=True)
    flight_id = Column(String(20), ForeignKey(FlightSchedule.id), primary_key=True)
    delayed = Column(Float, nullable=False)
    note = Column(String(255))


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    quantity = Column(Integer, default=0)
    details = relationship('TicketDetail', backref='receipt', lazy=True)


class TicketDetail(BaseModel):
    __tablename__ = 'ticket_detail'

    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    user_name = Column(String(100), nullable=False)
    passport = Column(Integer, nullable=False)
    telephone = Column(Integer, nullable=False)
    ticket_class = Column(String(100), nullable=False)
    price = Column(Float, default=0)


# if __name__ == '__main__':
    # db.create_all()

    # password = str(hashlib.md5("abcd1234".encode('utf-8')).hexdigest())
    # admin1 = User(last_name="Pham Quang", first_name="Minh", user_name="admin",
    #               password=password, email='minhpq123@gmail.com', phone_number='098765432', passport='798547640',
    #               image='https://res.cloudinary.com/dnwauajh9/image/upload/v1638608909/admin-image_dnghms.jpg',
    #               user_role=UserRole.ADMIN)
    # admin2 = User(last_name="Trần Thị", first_name="Nở", user_name="user",
    #               password=password, email='publicmail1009@gmail.com', phone_number='0987654321', passport='987654321',
    #               image='https://res.cloudinary.com/dnwauajh9/image/upload/v1639316867/download_bliziv.png',
    #               user_role=UserRole.USER)

    # for i in range(10):
    #     airport = Airport(id='AIR' + str(i), name='Airport' + str(i), address='Location' + str(i))
    #     db.session.add(airport)
    # db.session.add(admin2)
    # db.session.commit()
    # db.metadata.clear()
