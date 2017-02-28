# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

from application import app, db, user_datastore
from flask_security.utils import encrypt_password
from application.domain import models

db.init_app(app)
# admin = models.Role(name="Admin")
# user = models.Role(name="User")
# guest = models.Role(name="Guest")

# root = models.User(email="superuser", password="")
with app.app_context():
    admin_role = user_datastore.create_role(name="Admin")
    user_datastore.create_role(name="User")
    user_datastore.create_role(name="Guest")

    created_user = user_datastore.create_user(email='superuser', password=encrypt_password(''))
    user_datastore.add_role_to_user(created_user, admin_role)

    # root.roles = [admin]
    # db.session.add(root)

    db.session.commit()