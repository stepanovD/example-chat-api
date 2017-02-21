# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

from application import app, db
from application.domain import models

db.init_app(app)
guest = models.Role(role_name="Guest")
user = models.Role(role_name="User")
admin = models.Role(role_name="Admin")

root = models.User(login="superuser", password_hash="d41d8cd98f00b204e9800998ecf8427e", role_id=3)
with app.app_context():
    db.session.add(guest)
    db.session.add(user)
    db.session.add(admin)

    db.session.add(root)

    db.session.commit()