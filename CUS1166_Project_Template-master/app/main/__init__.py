# Imports the Blueprint class from flask.
from flask import Blueprint
from app.main import routes

bp = Blueprint('main',__name__, template_folder='../main/templates')

