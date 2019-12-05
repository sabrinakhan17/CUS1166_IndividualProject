# Imports the Blueprint class from flask.
from flask import Blueprint

bp = Blueprint('main',__name__, template_folder='../main/templates')

from app.main import routes