import click
from entregator.ext.db import db, models
from tabulate import tabulate

def init_app(app):

    @app.cli.command()
    def create_db():
        '''Esse comando inicializa o banco de dados'''
        db.create_all()

    @app.cli.command()
    @click.option('--email', '-e')
    @click.option('--passwd', '-p')
    @click.option('--admin', '-a', is_flag=True, default=False)
    def add_user(email, passwd, admin):
        '''Adiciona usuario'''
        user = models.User(
            email=email,
            passwd=passwd,
            admin=admin
        )
        db.session.add(user)
        db.session.commit()

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