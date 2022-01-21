from flask_restx import fields

from stores_management_app.web.products.dto import ProductDto
from stores_management_app.web.shops import shop_ns


class ShopDto:
    shop = shop_ns.model(
        "Shop object",
        {
            "id": fields.String(required=True),
            "name": fields.String(required=True),
            "address": fields.String(required=True),
            "products": fields.Nested(ProductDto.product, many=True)
        }
    )

    data_resp = shop_ns.model(
        "Shops Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "shops": fields.Nested(shop, required=True, many=True)
        }
    )

    add_shop_success = shop_ns.model(
        "Add Shop Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "shop": fields.Nested(shop, required=True)
        }
    )

    add_shop = shop_ns.model(
        " Add Shop object",
        {
            "name": fields.String(required=True),
            "address": fields.String(required=True)
        }
    )
