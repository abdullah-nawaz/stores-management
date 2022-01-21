from flask import request
from flask_restx import Resource

from . import shop_ns
from .dto import ShopDto
from .service import ShopService
from ..common.utils import token_required

data_resp = ShopDto.data_resp
add_shop = ShopDto.add_shop
add_shop_success = ShopDto.add_shop_success


@shop_ns.route("/shops")
class UserGet(Resource):
    @token_required
    @shop_ns.doc(security='api_key')
    @shop_ns.doc(
        "Get all shops for a user",
        responses={
            200: ("Shop data successfully sent", data_resp),
            404: "User not found!",
            204: "No shops for the user",
        },
    )
    def get(self, user_id):
        """ Get a specific user's shops data """
        return ShopService.get_shops_data(user_id)

    @token_required
    @shop_ns.doc(security='api_key')
    @shop_ns.doc(
        "Add Shop",
        responses={
            200: ("Shop successfully added for user.", add_shop_success),
            400: "Malformed data or validations failed.",
        },
    )
    @shop_ns.expect(add_shop, validate=True)
    def post(self, user_id):
        # Grab the json data
        register_data = request.get_json()
        return ShopService.add_shop_data(user_id, register_data)
