from entregator.ext.db.models import Category, Store
from entregator.ext.auth.controller import alter_order, alter_order_items, create_order_items


def categorias_menu():
    return Category.query.all()


def stores(lim: int=None):
    if lim == None:
         stores = Store.query.all()
    else:
        stores = Store.query.filter(Store.id < lim)
    return stores


def cart_params(order):
    order_items = order.order_items.all()
    items_list = []
    tot = 0
    for item in order_items:
        items_list.append({'name': item.items.name, 'quantidade': item.quant, 'preco': item.items.price, 'id': item.id, 'item_id': item.items.id})
        tot += item.items.price * item.quant
    return items_list, tot


def evaluate_order(loja, order):
    if int(loja) != order.store_id:
        ordered_items = order.order_items.all()

        if ordered_items:
            return 'O seu pedido deve ser todo apenas de uma loja!'
        else:
            alter_order(id=order.id, store_id=loja)


def evaluate_items_order(quantidade, order, comida):
    existing_item = order.order_items.filter_by(items_id=comida).first()

    if existing_item:
        alter_order_items(id=existing_item.id, quant=quantidade)
    else:
        create_order_items(order=order, items_id=comida, quant=quantidade)