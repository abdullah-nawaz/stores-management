from flask import Blueprint
from flask_restx import Namespace

stores_management_product = Blueprint("products", __name__)

product_ns = Namespace("stores_management_product", description="Product related operations.")

from stores_management_app.web.products import api
