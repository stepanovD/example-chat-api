# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

import datetime
from application.password import generate_password_hash, check_password_hash
from application import db
from flask.ext.security import UserMixin, RoleMixin

# ROLE_GUEST = 0
# ROLE_STUDENT = 1
# ROLE_TEACHER = 2
# ROLE_EDITOR = 3
# ROLE_ADMIN = 4

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Role %r>' % (self.name)

    def is_guest(self):
        return self.role_name == "Guest"

    def is_user(self):
        return self.role_name == "User"

    def is_admin(self):
        return self.role_name == "Admin"

    def show_admin_panel(self):
        return self.is_admin()

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

ChatUsers = db.Table('chat_users', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary="roles_users", backref=db.backref('users', lazy='dynamic'))
    chats = db.relationship('Chat', secondary="chat_users", backref="chats", lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.email)

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