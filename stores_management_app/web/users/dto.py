from flask_restx import fields

from stores_management_app.web.users import user_ns


class UserDto:
    user = user_ns.model(
        "User object",
        {
            "email": fields.String(required=True),
            "registered_on": fields.String(required=True)
        },
    )

    data_resp = user_ns.model(
        "User Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(user, required=True),
        },
    )
