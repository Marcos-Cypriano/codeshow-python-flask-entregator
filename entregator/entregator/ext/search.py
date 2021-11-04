import flask_whooshalchemy3 as wa
from .db.models import Store, Items

def init_app(app):
    wa.search_index(app, Store)
    wa.search_index(app, Items)