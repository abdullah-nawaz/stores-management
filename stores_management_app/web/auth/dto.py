from flask_restx import fields

from stores_management_app.web.auth import auth_namespace


class AuthDto:
    user_obj = auth_namespace.model(
        "User object",
        {
            "email": fields.String,
            "registered_on": fields.String
        },
    )

    auth_login = auth_namespace.model(
        "Login data",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True)
        },
    )

    auth_register = auth_namespace.model(
        "Registration data",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True)
        },
    )

    auth_success = auth_namespace.model(
        "Auth success response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "access_token": fields.String,
            "user": fields.Nested(user_obj)
        },
    )
