from flask_jwt_extended import jwt_required
from flask_restx import Resource

from . import user_ns
from .dto import UserDto
from .service import UserService
from ..common.utils import token_required

data_resp = UserDto.data_resp


@user_ns.route("/users/<email>")
class UserGet(Resource):
    @token_required
    @user_ns.doc(security='api_key')
    @user_ns.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", data_resp),
            404: "User not found!",
        },
    )
    @jwt_required()
    def get(self, email):
        """ Get a specific user's data by their username """
        return UserService.get_user_data(email)
