from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin.contrib.sqla import filters
from entregator.ext.db.models import User
from entregator.ext.db import db
from flask import flash


def format_user(self, request, user, *args):
    return user.email.split('@')[0]


class UserAdmin(ModelView):
    '''Interface do usuário admin'''

    column_formatters = {'email': format_user}
    column_list = ['admin', 'email']
    column_searchable_list = ['email']
    column_filters = [
        'email',
        'admin',
        filters.FilterLike(User.email, 'dominio', options=(('gmail', 'Gmail'), ('uol', 'Uol')))
        ]

    can_edit = False
    can_create = True
    can_delete = True

    @action(
        'toggle_admin',
        'Toggle Admin Status',
        'Are you sure?'
    )
    def toggle_admin_status(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        for user in users:
            user.admin = not user.admin
        db.session.commit()
        flash(f'Alteração no campo admin dos {len(users)} usuários , executada com sucesso!', 'success')


    @action(
        'send_email',
        'Send emails',
        'Are you sure?'
    )
    def send_email(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        #Redirecionar para um formulário de email, enviar e confirmar quantos foram com sucesso
        flash(f'Alteração no campo admin dos {len(users)} usuários , executada com sucesso!', 'success')