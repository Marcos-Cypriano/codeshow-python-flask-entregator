from flask import Flask
from entregator.ext import site
from entregator.ext import config
from entregator.ext import toolbar

def create_app():
    app = Flask(__name__)
    config.init_app(app)    
    toolbar.init_app(app)    
    site.init_app(app)    
    return app