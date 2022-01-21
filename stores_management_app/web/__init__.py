from flask import Blueprint, Flask
from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from config import flask_config
from stores_management_app.web.common.consts import authorizations

compress = Compress()
db = SQLAlchemy()
api = Api()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(environment):
    app = Flask(__name__)
    config = flask_config[environment]
    app.config.from_object(config)
    app.logger.setLevel(config.LOGGING_LEVEL_MAPPED)
    api.init_app(app)
    jwt.init_app(app)
    compress.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    db.app = app
    jwt._set_error_handler_callbacks(api)

    base_bp = Blueprint('store-management', __name__)
    base_api = Api(base_bp, title='Store Management', description='Store Management routes',
                   authorizations=authorizations, security='api_key')

    from stores_management_app.web.auth import auth_bp
    from stores_management_app.web.users import stores_management_user
    from stores_management_app.web.shops import stores_management_shop
    from stores_management_app.web.products import stores_management_product

    app.register_blueprint(base_bp, url_prefix="/v1/store-management")
    app.register_blueprint(auth_bp, url_prefix="/v1/store-management")
    app.register_blueprint(stores_management_user, url_prefix="/v1/store-management")
    app.register_blueprint(stores_management_shop, url_prefix="/v1/store-management")
    app.register_blueprint(stores_management_product, url_prefix="/v1/store-management")

    from stores_management_app.web.users import user_ns
    from stores_management_app.web.auth import auth_namespace
    from stores_management_app.web.shops import shop_ns
    from stores_management_app.web.products import product_ns

    base_api.add_namespace(user_ns)
    base_api.add_namespace(auth_namespace)
    base_api.add_namespace(shop_ns)
    base_api.add_namespace(product_ns)

    return app
