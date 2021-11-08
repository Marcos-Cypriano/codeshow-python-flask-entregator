import click
from tabulate import tabulate
from entregator.ext.db import db, models
from entregator.ext.auth.controller import create_user


def init_app(app):

    @app.cli.command()
    def create_db():
        '''Esse comando inicializa o banco de dados'''
        db.create_all()

    @app.cli.command()
    def drop_db():
        '''Esse comando limpa o banco de dados'''
        db.drop_all()

    @app.cli.command()
    @click.option('--email', '-e')
    @click.option('--passwd', '-p')
    @click.option('--admin', '-a', is_flag=True, default=False)
    def add_user(email, passwd, admin):
        '''Adiciona usuario'''
        create_user(email=email, passwd=passwd, admin=admin)

        click.echo(f'Usuário {email} criado com sucesso!')

    @app.cli.command()
    def listar_pedidos():
        click.echo('lista de pedidos ')
        
    @app.cli.command()
    def listar_usuarios():
        users = models.User.query.all()
        lista = []
        for user in users:
            lista.append(['name', user])

        click.echo(f'lista de usuarios\n{tabulate(lista)}')