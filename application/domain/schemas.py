__author__ = 'dmitry'
from application import ma
from models import *

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'login', '_links')
        model = User

    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.user', user_id='<id>'),
        'role': ma.URLFor('api.role', role_id='<role_id>'),
        'chats': ma.URLFor('api.chats'),
        'logout': ma.URLFor('api.logout')
    })

class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role

class ChatSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', '_links')
        # model = Chat

    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.chat', chat_id='<id>'),
        'users': ma.URLFor('api.chat_users', chat_id='<id>'),
        'messages': ma.URLFor('api.chat_messages', chat_id='<id>'),
        'owner': ma.URLFor('api.user', user_id='<owner_id>')
    })


class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content','timestamp', 'readed', '_links')
        # model = Message

    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.message', message_id='<id>'),
        'author': ma.URLFor('api.user', user_id='<user_id>'),
        'chat': ma.URLFor('api.chat', chat_id='<chat_id>')
    })
