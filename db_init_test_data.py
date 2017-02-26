# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

import random, time
from application import app, db
from application.domain import models

db.init_app(app)

user = models.User(login="user", password_hash="d41d8cd98f00b204e9800998ecf8427e", role_id=2)
guest = models.User(login="guest", password_hash="d41d8cd98f00b204e9800998ecf8427e", role_id=1)

chat = models.Chat(title="test chat", owner_id=1)

private_message = models.Message(content="test private message", chat_id=1, user_id=1)
shared_messages = []
user_ids = [1, 2, 3]

for i in range(1, 50):
        shared_messages.append(models.Message(content="test message %d" % i, user_id=random.choice(user_ids)))

with app.app_context():
    db.session.add(user)
    db.session.add(guest)

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