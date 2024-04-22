from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    items_to_buy = db.relationship('ToBuy', backref='User')
    items_bought = db.relationship('Bought', backref='User')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Since we named our primary key "user_id", instead of "id", we have to override the
    # get_id() from the UserMixin to return the id, and it has to be returned as a string
    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"user(id='{self.user_id}', '{self.username}', '{self.email}')"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ToBuy(db.Model):
    __tablename__ = 'ToBuy'
    item_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    item = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Bought(db.Model):
    __tablename__ = 'Bought'
    item_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    item = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)