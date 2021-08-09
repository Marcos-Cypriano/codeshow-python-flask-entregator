'''CICLO DE VIDA DE UM APLICATIVO FLASK (CONTEXTOS)''' 

# 1 CONFIGURAÇÃO
from flask import Flask

def create_app():
    app = Flask(__name__)

    ## Adicionar configurações
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DB_URI'] = 'mysql://...'

    ## Registrar rotas
    @app.route('/path')
    def funcao():
        ...

    app.add_url_rule('/path', funcao)

    ## Inicilaizar extensões
    from flask_admin import Admin
    Admin.init_app(app)

    ## Registrar blueprints
    app.register_blueprint(...)

    ## Adicionar hooks
    @app.before_request(...)
    @app.error_handler(...)

    ## Chamar outras factories
    views.init_app(app)

    return app

# 2 APP CONTEXT
## App pronto só esperando o WSGI chamar (flask run)
from flask import current_app, g

## Testar
'''app.test_client
debug
objetos globais do Flask (request, session, g)
Hooks'''


# 3 REQUEST CONTEXT
## Aqui um cliente está requisitando 
## Usar globais do Flask
from flask import request, session, g
request.args
request.form
