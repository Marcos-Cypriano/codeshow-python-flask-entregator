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

    '''def save(self):
        db.session.add(self)
        db.session.commit()'''
    
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

    def __repr__(self):
        return '%r' % (self.name)


class Store(db.Model):
    __tablename__ = "store"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode, unique=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    active = db.Column('active', db.Boolean)

    user = db.relationship('User', foreign_keys=user_id)
    category = db.relationship('Category', foreign_keys=category_id)

    def __repr__(self):
        return '%r' % (self.name)


class Items(db.Model):
    __tablename__ = "items"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    image = db.Column('image', db.Unicode)
    price = db.Column('price', db.Numeric(4,2))
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
    available = db.Column('available', db.Boolean)

    store = db.relationship('Store', foreign_keys=store_id)

    def __repr__(self):
        return '%r' % (self.name)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime)
    completed = db.Column('completed', db.Boolean)
    expired = db.Column('expired', db.Boolean)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('store.id'))
    address_id = db.Column('address_id', db.Integer, db.ForeignKey('address.id'))

    user = db.relationship('User', foreign_keys=user_id)
    store = db.relationship('Store', foreign_keys=store_id)
    address = db.relationship('Address', foreign_keys=address_id)

    def __repr__(self):
        return '%r' % (self.id)

class OrderItems(db.Model):
    __tablename__ = "order_items"
    id = db.Column('id', db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
    items_id = db.Column('items_id', db.Integer, db.ForeignKey('items.id'))
    quant = db.Column('quant', db.Integer)

    order = db.relationship('Order', foreign_keys=order_id)
    items = db.relationship('Items', foreign_keys=items_id)


class Checkout(db.Model):
    __tablename__ = "checkout"
    id = db.Column('id', db.Integer, primary_key=True)
    payment = db.Column('payment', db.Unicode)
    total = db.Column('total', db.Numeric(4,2))
    created_at = db.Column('created_at', db.DateTime)
    completed = db.Column('completed', db.Boolean)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))

    order = db.relationship('Order', foreign_keys=order_id)


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column('id', db.Integer, primary_key=True)
    zip = db.Column('zip', db.Unicode)
    country = db.Column('country', db.Unicode)
    address = db.Column('address', db.Unicode)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __repr__(self):
        return '%r' % (self.id)