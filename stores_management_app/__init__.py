from contextlib import contextmanager

from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLAlchemyConfig

compress = Compress()
db = SQLAlchemy()

Session = sessionmaker(bind=create_engine(
    SQLAlchemyConfig.SQLALCHEMY_DATABASE_URI, pool_size=SQLAlchemyConfig.SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLAlchemyConfig.SQLALCHEMY_MAX_OVERFLOW, pool_recycle=SQLAlchemyConfig.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=SQLAlchemyConfig.SQLALCHEMY_POOL_TIMEOUT))


@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
