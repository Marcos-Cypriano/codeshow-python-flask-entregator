from datetime import datetime
from whoosh.analysis import StemmingAnalyzer

from entregator.ext.db import db
from entregator.ext.admin import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.Unicode, unique=True)
    passwd = db.Column('passwd', db.Unicode)
    admin = db.Column('admin', db.Boolean)

    addresses = db.relationship('Address', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    stores = db.relationship('Store', backref='user', lazy='dynamic')

    #PROPRIEDADES DO FLASK-LOGIN    
    @property
    def is_authenticated(self):
        if self.admin == 1:
            return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __repr__(self) -> str:
        return self.email


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode, unique=True)
    on_menu = db.Column('on_menu', db.Boolean)

    stores = db.relationship('Store', backref='category', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.name)


class Store(db.Model):
    __tablename__ = "store"
    __searchable__ = ['name']
    __analyzer__ = StemmingAnalyzer()

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode, unique=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    active = db.Column('active', db.Boolean)

    items = db.relationship('Items', backref='store', lazy='dynamic')
    orders = db.relationship('Order', backref='store', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.name)


class Items(db.Model):
    __tablename__ = "items"
    __searchable__ = ['name']
    __analyzer__ = StemmingAnalyzer()

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    image = db.Column('image', db.Unicode)
    price = db.Column('price', db.Numeric(10,2))
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
    available = db.Column('available', db.Boolean)

    order_items = db.relationship('OrderItems', backref='items', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.name)


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column('completed', db.Boolean)
    expired = db.Column('expired', db.Boolean)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
    address_id = db.Column('address_id', db.Integer, db.ForeignKey('address.id'))

    order_items = db.relationship('OrderItems', backref='order', lazy='dynamic')
    checkout = db.relationship('Checkout', backref='order', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.id)

class OrderItems(db.Model):
    __tablename__ = "order_items"

    id = db.Column('id', db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
    items_id = db.Column('items_id', db.Integer, db.ForeignKey('items.id'))
    quant = db.Column('quant', db.Integer)


class Checkout(db.Model):
    __tablename__ = "checkout"

    id = db.Column('id', db.Integer, primary_key=True)
    payment = db.Column('payment', db.Unicode)
    total = db.Column('total', db.Numeric(10,2))
    created_at = db.Column('created_at', db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column('completed', db.Boolean)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column('id', db.Integer, primary_key=True)
    zip = db.Column('zip', db.Unicode)
    country = db.Column('country', db.Unicode)
    address = db.Column('address', db.Unicode)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))

    orders = db.relationship('Order', backref='address', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.id)