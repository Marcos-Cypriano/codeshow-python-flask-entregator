import views
from flask import Flask


def create_app():
    '''FACTORY PRINCIPAL'''
    app = Flask(__name__)
    views.init_app(app)
    return app

