from sqlalchemy import create_engine
import datetime

from app import db, app
import traceback

from sqlalchemy import event


def init_app(app):
    db.app = app
    db.init_app(app)
    return db


def create_table(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


cart = db.Table('cart',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(200), unique=True, nullable=False)
    items_in_cart = db.relationship('Product', secondary=cart, backref='cart-products')


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    discount = db.Column(db.Float)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    cgst = db.Column(db.Float)
    sgst = db.Column(db.Float)
    invoice_total = db.Column(db.Float, nullable=False)
    billing_address = db.relationship('BillingAddress', backref='order', lazy=True)
    shipping_address = db.relationship('ShippingAddress', backref='order', lazy=True)


class OrderProduct(db.Model):
    __tablename__ = "order-product"
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey('order.id'))
    pid = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)


class BillingAddress(db.Model):
    __tablename__ = "billing_address"
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey("order.id"))
    full_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    house_no = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(200), nullable=False)
    landmark = db.Column(db.String(200))
    town = db.Column(db.String(200), nullable=False)


class ShippingAddress(db.Model):
    __tablename__ = "shipping_address"
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey("order.id"))
    full_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    house_no = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(200), nullable=False)
    landmark = db.Column(db.String(200))
    town = db.Column(db.String(200), nullable=False)


init_app(app)
create_table(app)
