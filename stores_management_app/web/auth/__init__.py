from flask import Blueprint
from flask_restx import Namespace

auth_bp = Blueprint("auth", __name__)

auth_namespace = Namespace("auth_bp", description="Authenticate and receive tokens.")

from stores_management_app.web.auth import api
