import hashlib

from saleapp import db
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum


class BaseMode(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseMode):
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(50), nullable=False)
    user_name = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)


if __name__ == '__main__':
    db.create_all()

    # password = str(hashlib.md5("abcd1234".encode('utf-8')).hexdigest())
    # admin1 = User(first_name="Tat Quang", last_name="Kiet", user_name="admin",
    #               password=password, email='tatquangkiet@gmail.com',
    #               image='https://res.cloudinary.com/dnwauajh9/image/upload/v1638608909/admin-image_dnghms.jpg',
    #               user_role=UserRole.ADMIN)

    # db.session.add(admin1)
    # db.session.commit()