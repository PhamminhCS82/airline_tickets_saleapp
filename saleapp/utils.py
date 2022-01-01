import hashlib
from models import User, UserRole
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


def add_user(last_name, first_name, user_name, password, email, image):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    new_user = User(last_name=last_name.strip(),
                    first_name=first_name.strip(),
                    user_name=user_name.strip(),
                    password=password,
                    email=email.strip(),
                    image=image)
    db.session.add(new_user)
    db.session.commit()
