import logging
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class CompressionConfig:
    COMPRESS_MIMETYPES = ["application/json"]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class EncryptionConfig:
    SALT_LENGTH = 32
    DERIVATION_ROUNDS = 100000
    BLOCK_SIZE = 16
    KEY_SIZE = 32
    SECRET = "nw2FrNshF"


class PaginationConfig:
    DEFAULT_LIMIT = 10
    MAX_PAGE_LIMIT = 50


class DatabaseConfig:
    STORES_MANAGEMENT_DB_PARAMS = {
        "STORES_MANAGEMENT_DB_HOST": os.environ.get("ENV_STORES_MANAGEMENT_DB_HOST", "storesmanagementdb"),
        "STORES_MANAGEMENT_DB_PORT": os.environ.get("ENV_STORES_MANAGEMENT_DB_PORT", "3306"),
        "STORES_MANAGEMENT_DB_NAME": os.environ.get(
            "ENV_STORES_MANAGEMENT_DB_NAME", "storesmanagementdb"
        ),
        "STORES_MANAGEMENT_DB_MYSQL_USER": os.environ.get("ENV_STORES_MANAGEMENT_DB_MYSQL_USER", "root"),
        "STORES_MANAGEMENT_DB_MYSQL_PASSWORD": os.environ.get(
            "ENV_STORES_MANAGEMENT_DB_MYSQL_PASSWORD", "admin123"
        ),
    }
    STORES_MANAGEMENT_DB_URI = (
        "mysql+mysqldb://{STORES_MANAGEMENT_DB_MYSQL_USER}:{STORES_MANAGEMENT_DB_MYSQL_PASSWORD}@"
        "{STORES_MANAGEMENT_DB_HOST}:{STORES_MANAGEMENT_DB_PORT}/{STORES_MANAGEMENT_DB_NAME}".format(
            **STORES_MANAGEMENT_DB_PARAMS)
    )


class SQLAlchemyConfig(DatabaseConfig):
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.STORES_MANAGEMENT_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", "400"))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", "450"))
    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", "5"))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", "0"))
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
        "pool_timeout": SQLALCHEMY_POOL_TIMEOUT,
        "pool_size": SQLALCHEMY_POOL_SIZE,
        "max_overflow": SQLALCHEMY_MAX_OVERFLOW
    }


class FlaskConfig(CompressionConfig):
    __LOGGING_LEVEL_MAPPER = {
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    try:
        LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
        LOGGING_LEVEL_MAPPED = __LOGGING_LEVEL_MAPPER[LOGGING_LEVEL]
    except KeyError:
        raise ValueError(f"LOGGING_LEVEL should be one of {list(__LOGGING_LEVEL_MAPPER.keys())}")

    SECRET_KEY = os.environ.get("SECRET_KEY", "my_precious_stores_management")
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # File upload setting
    MAX_CONTENT_LENGTH = 2048 * 2048

    @staticmethod
    def init_app(app):
        pass


class FlaskDevelopmentConfig(FlaskConfig, SQLAlchemyConfig):
    DEBUG = True
    PORT = 8082
    USE_SSL = os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class FlaskProductionConfig(FlaskConfig, SQLAlchemyConfig):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        FlaskConfig.init_app(app)


flask_config = {
    "DEVELOPMENT": FlaskDevelopmentConfig,
    "PRODUCTION": FlaskProductionConfig,
    "default": FlaskDevelopmentConfig
}
