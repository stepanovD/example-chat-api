# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# administrator list
CSRF_ENABLED = True

SECRET_KEY = '09f6e1d21c5343de956791918952c71d'
SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'X-Auth-Token'