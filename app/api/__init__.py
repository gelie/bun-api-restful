from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/bungeni/api/v1')

from app.api import routes
