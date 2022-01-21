from flask import Blueprint
from flask_restx import Namespace

stores_management_shop = Blueprint("shops", __name__)

shop_ns = Namespace("stores_management_shop", description="Shop related operations.")

from stores_management_app.web.shops import api
