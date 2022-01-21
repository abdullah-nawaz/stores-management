import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from stores_management_app import db


class Shop(db.Model):
    ID_KEY = "id"
    NAME_KEY = "name"
    ADDRESS_KEY = "address"
    PRODUCTS_KEY = "products"

    __tablename__ = 'shops'

    id = Column(String(32), primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)

    user_id = Column(String(32), ForeignKey('users.id'), nullable=False)

    products = relationship('Product', backref='shop', cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, name, address):
        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.address = address

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.NAME_KEY: self.name,
            self.ADDRESS_KEY: self.address,
            self.PRODUCTS_KEY: [product.to_json for product in self.products.all()]
        }


class Product(db.Model):
    ID_KEY = "id"
    TITLE_KEY = "title"
    DATE_ADDED_KEY = "date_added"
    DATE_UPDATED_KEY = "date_updated"
    IMAGE_KEY = "image"
    DESCRIPTION_KEY = "description"
    PRICE_KEY = "price"

    __tablename__ = 'products'

    id = Column(String(32), primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    date_added = Column(DateTime, unique=True, nullable=False)
    date_updated = Column(DateTime, unique=True)
    image = Column(Text)
    description = Column(Text)
    price = Column(Integer, nullable=False)

    shop_id = Column(String(32), ForeignKey('shops.id'), nullable=False)

    def __init__(self, title, price, date_updated=None, image=None, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.date_added = datetime.utcnow()
        self.price = price
        self.date_updated = date_updated
        self.image = image
        self.description = description

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.TITLE_KEY: self.title,
            self.DATE_ADDED_KEY: str(self.date_added),
            self.PRICE_KEY: self.price,
            self.DATE_UPDATED_KEY: str(self.date_updated),
            self.IMAGE_KEY: self.image,
            self.DESCRIPTION_KEY: self.description
        }
