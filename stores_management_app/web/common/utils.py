from functools import wraps

from flask import request

from stores_management_app.models import BlacklistToken


def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object


def validation_error(status, errors):
    response_object = {"status": status, "errors": errors}

    return response_object


def err_resp(msg, reason, code):
    err = message(False, msg)
    err["error_reason"] = reason
    return err, code


def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import current_app
        import jwt

        token = None
        if 'Authorization' in request.headers:
            if "Bearer " not in request.headers["Authorization"]:
                return {'message': 'Token is missing.'}, 401
            token = request.headers['Authorization']
            try:
                key = current_app.config.get("SECRET_KEY")
                payload = jwt.decode(token.split("Bearer")[1].strip(), key, algorithms="HS256")
                args = [*args, payload["user_id"]]
                is_blacklisted_token = BlacklistToken.check_blacklist(token.split("Bearer")[1].strip())
                if is_blacklisted_token:
                    return 'Token blacklisted. Please log in again.', 401

            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.', 401
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.', 401

        if not token:
            return {'message': 'Token is missing.'}, 401

        return f(*args, **kwargs)

    return decorated
