import os
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask import flash
from sqlalchemy.exc import IntegrityError
from entregator.ext.db.models import Checkout, Items, Order, OrderItems, User, Address
from entregator.ext.db import db


ALG = 'pbkdf2:sha256'
#Mudar para o Models
def create_user(email: str, passwd: str, admin: bool=False) -> User:
    user = User(email=email, passwd=generate_password_hash(passwd, ALG), admin=admin)
    
    db.session.add(user)
    try :
        db.session.commit()
    except IntegrityError:
        return flash('Este usuário já existe, tente outro!')
        
    return user


def save_user_photo(filename, filestorage):
    '''Saves user photo in .uploads/user/dfhioadihow.ext'''
    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    #VERIFICAR se o diretório existe; criar caso não exista
    filestorage.save(filename)


def add_address(zip, country, address, user_id):
    endereco = Address(zip=zip, country=country, address=address, user_id=user_id)

    db.session.add(endereco)
    db.session.commit()

    return endereco


def create_order(completed: bool=False, expired: bool=False, user_id = int, store_id = int, address_id: int=None) -> Order:
    order = Order(completed=completed, expired=expired, user_id=user_id, store_id=store_id, address_id=address_id)
    
    db.session.add(order)
    db.session.commit()
        
    return order


def alter_order(created_at: datetime=datetime.datetime.utcnow(), id = int, store_id = int) -> Order:
    order = Order.query.get(id)
    order.store_id = store_id
    order.created_at = created_at
    
    db.session.commit()
        
    return order


def alter_address_order(id= int, address_id = int) -> Order:
    order = Order.query.get(id)
    order.address_id = address_id
    
    db.session.commit()
        
    return order


def create_order_items(order, items_id = int, quant = int) -> OrderItems:
    order_items = OrderItems(order_id=order.id, items_id=items_id, quant=quant)
    
    db.session.add(order_items)
    db.session.commit()
        
    return order_items


def alter_order_items(id = int, quant = int) -> OrderItems:
    order_items = OrderItems.query.get(id)
    order_items.quant = quant

    db.session.commit()
        
    return order_items


def delete_order_items(items_id = int) -> OrderItems:
    OrderItems.query.filter_by(id=items_id).delete()
    db.session.commit()
        
    return 'Item removido do carrinho!'
        

def delete_address(endereco = int) -> Address:
    Address.query.filter_by(id=endereco).delete()
    db.session.commit()
        
    return 'Item removido do carrinho!'


def complete_order(order_id = int, completed = bool) -> Order:
    order = Order.query.get(order_id)
    order.completed = completed

    db.session.commit()

    return order


def create_checkout(order, payment = str, completed: bool=False):
    items = order.order_items.all()
    tot = 0
    items_list = []
    for item in items:
        prato = Items.query.get(item.items_id)
        items_list.append({'name': prato.name, 'quantidade': item.quant})
        tot += prato.price * item.quant

    checkout = Checkout(payment=payment, total=tot, completed=completed, order_id=order.id)

    db.session.add(checkout)
    db.session.commit()

    return checkout