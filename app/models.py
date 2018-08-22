#encoding:utf-8
from app import db

class User(db.Model):

    __tablename__ = 'users'

    def __str__(self) -> str:
        return "User(name={}, password={}, age={})".format(self.username, self.password, self.age)

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(36))
    password = db.Column(db.String(36))
    age = db.Column(db.Integer)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'age': self.age
        }