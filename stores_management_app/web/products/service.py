from flask import current_app

from stores_management_app import db
from stores_management_app.models import Product
from stores_management_app.models.user_models import User
from stores_management_app.web.common.utils import err_resp, internal_err_resp, message


class ProductService:
    @staticmethod
    def get_products_data(user_id, shop_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return err_resp("User not found!", "user_404", 404)
        shop = user.shops.filter_by(id=shop_id).first()
        if not shop:
            return err_resp("Shop not found!", "Shops_404", 404)

        if not shop.products.all():
            return "No products in shop", 204

        try:
            products_data = [product.to_json() for product in shop.products.all()]

            resp = message(True, "Products data sent")
            resp["products"] = products_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_product_data(user_id, shop_id, data):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return err_resp("User not found!", "user_404", 404)

        shop = user.shops.filter_by(id=shop_id).first()
        if not shop:
            return err_resp("Shop not found!", "Shops_404", 404)

        # TODO: ADD validations later
        try:
            product = Product(**data)
            db.session.add(product)
            shop.products.append(product)
            db.session.commit()

            resp = message(True, "Products data added")
            resp["product"] = product.to_json()
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
