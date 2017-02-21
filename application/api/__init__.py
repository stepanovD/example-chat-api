__author__ = 'dmitry'

from flask import Blueprint

api = Blueprint('api', __name__, template_folder='templates')

import application.api.views
