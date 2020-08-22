from flask import Blueprint

bp = Blueprint("api.v1", __name__, url_prefix='/v1')

from . import images