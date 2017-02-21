# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

import datetime
from application.password import generate_password_hash, check_password_hash
from application import db

# ROLE_GUEST = 0
# ROLE_STUDENT = 1
# ROLE_TEACHER = 2
# ROLE_EDITOR = 3
# ROLE_ADMIN = 4

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % (self.role_name)

    def is_guest(self):
        return self.role_name == "Guest"

    def is_user(self):
        return self.role_name == "User"

    def is_admin(self):
        return self.role_name == "Admin"

    def show_admin_panel(self):
        return self.is_admin()

ChatUsers = db.Table('chat_users', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.SmallInteger, db.ForeignKey('role.id'))
    chats = db.relationship('Chat', secondary="chat_users", backref="chats", lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.login)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    users = db.relationship('User', secondary="chat_users", backref="users", lazy='dynamic')
    messages = db.relationship('Message', backref="messages", lazy='dynamic')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1200))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=True, default=None, index=True)
    readed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Message %r>' % (self.content)

    def is_readed(self):
        return self.readed