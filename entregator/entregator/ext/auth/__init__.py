from entregator.ext.db import db
from entregator.ext.auth.admin import UserAdmin, CategoryAdmin, StoreAdmin
from entregator.ext.admin import admin
from entregator.ext.db.models import User, Category, Store

def init_app(app):
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(StoreAdmin(Store, db.session))