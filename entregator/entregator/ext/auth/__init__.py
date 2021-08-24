from entregator.ext.db import db
from entregator.ext.auth.admin import UserAdmin
from entregator.ext.admin import admin
from entregator.ext.db.models import User

def init_app(app):
    admin.add_view(UserAdmin(User, db.session))