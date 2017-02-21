__author__ = 'dmitry'

from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from flask_marshmallow import Marshmallow

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from flask.ext.mail import Mail
mail = Mail(app)

from application.api import api


app.register_blueprint(api, url_prefix='/api')
# app.register_blueprint(main)

from application.domain.models import User, Role

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(404)
def page_not_found(e):
    return e, 404


