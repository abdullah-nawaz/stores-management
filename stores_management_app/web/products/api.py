from flask import request
from flask_restx import Resource

from . import product_ns
from .dto import ProductDto
from .service import ProductService
from ..common.utils import token_required

data_resp = ProductDto.data_resp
add_product = ProductDto.add_product
add_product_success = ProductDto.add_product_success


@product_ns.route("/products/<shop_id>")
class UserGet(Resource):
    @token_required
    @product_ns.doc(security='api_key')
    @product_ns.doc(
        "Get all products for a user and sho id provider",
        responses={
            200: ("Product data successfully sent", data_resp),
            404: "Shop oe user not found!",
            204: "No Products"
        },
    )
    def get(self, user_id, shop_id):
        """ Get a products data for user and shop ID provider """
        return ProductService.get_products_data(user_id, shop_id)

    @token_required
    @product_ns.doc(security='api_key')
    @product_ns.doc(
        "Add Product",
        responses={
            200: ("Product successfully added for user.", add_product_success),
            400: "Malformed data or validations failed.",
        },
    )
    @product_ns.expect(add_product, validate=True)
    def post(self, user_id, shop_id):
        # Grab the json data
        register_data = request.get_json()
        print(shop_id)
        return ProductService.add_product_data(user_id, shop_id, register_data)
