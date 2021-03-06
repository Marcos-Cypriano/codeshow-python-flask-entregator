from entregator.ext.db import db
from entregator.ext.auth.admin import MyAdminIndexView, UserAdmin, CategoryAdmin, StoreAdmin, ItemsAdmin, OrderAdmin, OrderItemsAdmin, AddressAdmin, CheckoutAdmin
from entregator.ext.admin import admin
from entregator.ext.db.models import Address, Checkout, Items, Order, OrderItems, User, Category, Store

def init_app(app):
    admin._set_admin_index_view(index_view=MyAdminIndexView(), endpoint='admin')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(AddressAdmin(Address, db.session))
    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(StoreAdmin(Store, db.session))
    admin.add_view(ItemsAdmin(Items, db.session))
    admin.add_view(OrderAdmin(Order, db.session))   
    admin.add_view(OrderItemsAdmin(OrderItems, db.session))  
    admin.add_view(CheckoutAdmin(Checkout, db.session))  