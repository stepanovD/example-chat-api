# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

import random, time
from application import app, db, user_datastore
from flask_security.utils import encrypt_password
from application.domain import models

db.init_app(app)

chat = models.Chat(title="test chat", owner_id=1)

private_message = models.Message(content="test private message", chat_id=1, user_id=1)
shared_messages = []
user_ids = [1, 2, 3]

for i in range(1, 50):
        shared_messages.append(models.Message(content="test message %d" % i, user_id=random.choice(user_ids)))

with app.app_context():
    user_role = models.Role.query.get(2)
    guest_role = models.Role.query.get(3)

    created_user = user_datastore.create_user(email='user', password=encrypt_password(''))
    user_datastore.add_role_to_user(created_user, user_role)

    created_guest = user_datastore.create_user(email='guest', password=encrypt_password(''))
    user_datastore.add_role_to_user(created_guest, guest_role)

    db.session.flush()

    chat.users = [models.User.query.get(1), models.User.query.get(2)]

    db.session.add(private_message)

    db.session.commit()

    for msg in shared_messages:
        print msg.content
        db.session.add(msg)
        db.session.flush()
        time.sleep(1)

    db.session.commit()

    print len(models.User.query.all())