__author__ = 'dmitry'
from schemas import *

user_schema = UserSchema(exclude=("password_hash"))
users_schema = UserSchema(many=True, exclude=("password_hash"))

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)