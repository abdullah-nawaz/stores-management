from flask import Blueprint
from flask_restx import Namespace

stores_management_user = Blueprint("users", __name__)

user_ns = Namespace("stores_management_user", description="User related operations.")

from stores_management_app.web.users import api
