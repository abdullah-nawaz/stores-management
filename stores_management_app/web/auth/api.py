from flask import request
from flask_restx import Resource

from . import auth_namespace
from .dto import AuthDto
from .service import AuthService

auth_success = AuthDto.auth_success


@auth_namespace.route("/login")
class AuthLogin(Resource):
    """ User login endpoint
    User registers then receives the user's information and access_token
    """

    auth_login = AuthDto.auth_login

    @auth_namespace.doc(security=None)
    @auth_namespace.doc(
        "Auth login",
        responses={
            200: ("Logged in", auth_success),
            400: "Validations failed.",
            403: "Incorrect password or incomplete credentials.",
            404: "Email does not match any account.",
        },
    )
    @auth_namespace.expect(auth_login, validate=True)
    def post(self):
        """ Login using email and password """
        # Grab the json data
        login_data = request.get_json()
        return AuthService.login(login_data)


@auth_namespace.route("/register")
class AuthRegister(Resource):
    """ User register endpoint
    User registers then receives the user's information and access_token
    """

    auth_register = AuthDto.auth_register

    @auth_namespace.doc(security=None)
    @auth_namespace.doc(
        "Auth registration",
        responses={
            200: ("Successfully registered user.", auth_success),
            400: "Malformed data or validations failed.",
        },
    )
    @auth_namespace.expect(auth_register, validate=True)
    def post(self):
        """ User registration """
        # Grab the json data
        register_data = request.get_json()
        return AuthService.register(register_data)
