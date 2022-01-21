from flask import current_app

from stores_management_app import db
from stores_management_app.models import Shop
from stores_management_app.models.user_models import User
from stores_management_app.web.common.utils import err_resp, internal_err_resp, message


class ShopService:
    @staticmethod
    def get_shops_data(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return err_resp("User not found!", "user_404", 404)

        if not user.shops.all():
            return "No shop for user", 204

        try:
            shops_data = [shop.to_json() for shop in user.shops.all()]

            resp = message(True, "Shops data sent")
            resp["shops"] = shops_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_shop_data(user_id, data):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return err_resp("User not found!", "user_404", 404)

        # TODO: ADD validations later
        try:
            shop = Shop(**data)
            db.session.add(shop)
            user.shops.append(shop)
            db.session.commit()

            resp = message(True, "Shop data added")
            resp["shop"] = shop.to_json()
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
