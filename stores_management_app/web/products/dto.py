from flask_restx import fields

from stores_management_app.web.products import product_ns


class ProductDto:
    product = product_ns.model(
        "Product object",
        {
            "id": fields.String(required=True),
            "title": fields.String(required=True),
            "date_added": fields.String(required=True),
            "date_updated": fields.String(required=False, allow_none=True),
            "image": fields.String(required=False, allow_none=True),
            "description": fields.String(required=False, allow_none=True),
            "price": fields.Integer(required=True)
        }
    )

    data_resp = product_ns.model(
        "Products Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "products": fields.Nested(product, required=True, many=True)
        }
    )

    add_product_success = product_ns.model(
        "Add Product Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "product": fields.Nested(product, required=True)
        }
    )

    add_product = product_ns.model(
        " Add Product object",
        {
            "title": fields.String(required=True),
            "date_updated": fields.String(required=False, allow_none=True),
            "image": fields.String(required=False, allow_none=True),
            "description": fields.String(required=False, allow_none=True),
            "price": fields.Integer(required=True)
        }
    )
