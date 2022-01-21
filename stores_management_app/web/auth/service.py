from datetime import datetime, timedelta

from flask import current_app
from flask_jwt_extended import create_access_token
import jwt

from stores_management_app.web.common.utils import message, err_resp, internal_err_resp
from stores_management_app.models.user_models import User

from stores_management_app import db


class AuthService:
    @staticmethod
    def login(data):
        # Assign vars
        email = data["email"]
        password = data["password"]

        try:
            # Fetch user data
            user = User.query.filter_by(email=email).first()
            if not user:
                return err_resp(
                    "The email you have entered does not match any account.",
                    "email_404",
                    404,
                )

            elif user and user.password == password:
                user_info = user.to_json()

                key = current_app.config.get("SECRET_KEY")
                access_token = jwt.encode({'user_id': user.id}, key, algorithm="HS256")

                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["user"] = user_info

                return resp, 200

            return err_resp(
                "Failed to log in, password may be incorrect.", "password_invalid", 401
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def register(data):
        print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        # Assign vars

        ## Required values
        email = data["email"]
        password = data["password"]

        ## Optional
        data_name = data.get("name")

        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            return err_resp("Email is already being used.", "email_taken", 403)

        try:
            new_user = User(
                email=email,
                password=password
            )

            db.session.add(new_user)

            # Load the new user's info
            user_info = new_user.to_json()

            # Commit changes to DB
            db.session.commit()

            # Create an access token
            access_token = create_access_token(identity=new_user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = user_info

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
