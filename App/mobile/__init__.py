from flask import Blueprint

mobile = Blueprint('mobile', __name__)

from . import views, errors
