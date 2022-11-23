from flask import Blueprint

checklist = Blueprint('checklist', __name__)

from . import views