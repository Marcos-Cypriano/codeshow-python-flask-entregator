'''EXTENSÃO DO FLASK'''

from flask import Flask

def init_app(app: Flask):
    '''FACTORY DE INICIALIZAÇÃO DE EXTENSÕES'''

    @app.route("/") #Views
    def index():
        return "<h1>Olá mundão!</h1>"

    @app.route("/contato")
    def sobre():
        return "<form><input type='text'>Contato</input></form>"