from flask_admin import Admin
from flask_login import LoginManager

admin = Admin()
login_manager = LoginManager()

def init_app(app):
    admin.name = app.config.get('ADMIN_NAME', 'Entregator')
    admin.template_mode = app.config.get('ADMIN_TEMPLATE_MODE', 'bootstrap2')
    admin.init_app(app)
    login_manager.init_app(app)
