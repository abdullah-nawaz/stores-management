from flask import current_app

from stores_management_app.models.user_models import User
from stores_management_app.web.common.utils import err_resp, internal_err_resp, message


class UserService:
    @staticmethod
    def get_user_data(user_id, email):
        """ Get user data by username """
        print(user_id)
        user = User.query.filter_by(id=user_id, email=email).first()
        if not user:
            return err_resp("User not found!", "user_404", 404)


        try:
            user_data = user.to_json()

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
