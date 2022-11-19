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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(200), unique=True, nullable=False)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(200), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'firebase_id': self.firebase_uid,
            'userName': self.userName,
            'email': self.email,
            'mobile': self.mobile,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    discount = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category': self.category,
            'unit_price': self.unit_price,
            'description': self.description,
            'image_url': self.image_url,
            'discount': self.discount,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date
        }


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='Cart')
    pid = db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'pid': self.pid,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    cgst = db.Column(db.Float)
    sgst = db.Column(db.Float)
    invoice_total = db.Column(db.Float, nullable=False)
    billing_address = db.relationship('BillingAddress', backref='order', lazy=True)
    shipping_address = db.relationship('ShippingAddress', backref='order', lazy=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'cgst': self.cgst,
            'sgst': self.sgst,
            'invoice_total': self.invoice_total,
            'billing_address': self.billing_address,
            'shipping_address': self.shipping_address,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date

        }


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey('order.id'))
    pid = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'oid': self.oid,
            'pid': self.pid,
            'quantity': self.quantity,
            'amount': self.amount,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date
        }


class BillingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_billing = db.relationship("User", backref="BillingAddress")
    oid = db.Column(db.Integer, db.ForeignKey("order.id"))
    full_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    house_no = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(200), nullable=False)
    landmark = db.Column(db.String(200))
    town = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'uid':self.uid,
            'oid': self.oid,
            'full_name': self.full_name,
            'country': self.country,
            'mobile': self.mobile,
            'pincode': self.pincode,
            'house_no': self.house_no,
            'area': self.area,
            'landmark': self.landmark,
            'town': self.town,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date
        }


class ShippingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_shipping = db.relationship("User", backref="ShippingAddress")
    oid = db.Column(db.Integer, db.ForeignKey("order.id"))
    full_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    house_no = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(200), nullable=False)
    landmark = db.Column(db.String(200))
    town = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'uid':self.uid,
            'oid': self.oid,
            'full_name': self.full_name,
            'country': self.country,
            'mobile': self.mobile,
            'pincode': self.pincode,
            'house_no': self.house_no,
            'area': self.area,
            'landmark': self.landmark,
            'town': self.town,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date

        }
