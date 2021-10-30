from entregator.ext.db.models import Category, Items, OrderItems, Store
from entregator.ext.auth.controller import alter_order, alter_order_items, create_order_items


def categorias_menu():
    return Category.query.all()


def stores(lim: int=None):
    if lim == None:
         stores = Store.query.all()
    else:
        stores = Store.query.filter(Store.id < lim)
    return stores


def cart_params(order_id):
    order_items = OrderItems.query.filter_by(order_id=order_id).all()
    items_list = []
    tot = 0
    for item in order_items:
        prato = Items.query.get(item.items_id)
        items_list.append({'name': prato.name, 'quantidade': item.quant, 'preco': prato.price, 'id': item.id, 'item_id': prato.id})
        tot += prato.price * item.quant
    return items_list, tot


def evaluate_order(loja, order):
    if int(loja) != order.store_id:
        ordered_items = OrderItems.query.filter_by(order_id=order.id).all()

        if ordered_items:
            return 'O seu pedido deve ser todo apenas de uma loja!'
        else:
            alter_order(id=order.id, store_id=loja)


def evaluate_items_order(quantidade, order_id, comida):
    existing_item = OrderItems.query.filter_by(order_id=order_id, items_id=comida).first()

    if existing_item:
        alter_order_items(id=existing_item.id, quant=quantidade)
    else:
        create_order_items(order_id=order_id, items_id=comida, quant=quantidade)

    return cart_params(order_id)