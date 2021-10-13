from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin.contrib.sqla import filters
from entregator.ext.db.models import User
from entregator.ext.db import db
from flask import flash, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView


def format_user(self, request, user, *args):
    return user.email.split('@')[0]

class MyAdminIndexView(AdminIndexView):
    #VISUALIZAÇÃO da página '/admin'
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash('Você não possui permissão para acessar. Entre com um perfil de administrador', 'error')
        return redirect(url_for('site.index'))


class UserAdmin(ModelView):
    '''Interface do usuário admin'''

    column_formatters = {'email': format_user}
    column_list = ['admin', 'email', 'passwd']
    column_searchable_list = ['email']
    column_filters = [
        'email',
        'admin',
        filters.FilterLike(User.email, 'dominio', options=(('gmail', 'Gmail'), ('uol', 'Uol')))
        ]

    can_edit = True
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


class CategoryAdmin(ModelView):

    column_list = ['on_menu', 'name']

    can_edit = False
    can_create = True
    can_delete = True


class StoreAdmin(ModelView):

    column_list = ['active', 'name', 'user', 'category']
    column_searchable_list = ['category_id']

    can_edit = True
    can_create = True
    can_delete = True


class ItemsAdmin(ModelView):
    #TENTAR alterar a busca para o nome do restaurante
    column_searchable_list = ['store_id']

    can_edit = True
    can_create = True
    can_delete = True


class OrderAdmin(ModelView):

    can_edit = True
    can_create = True
    can_delete = True


class OrderItemsAdmin(ModelView):

    can_edit = False
    can_create = True
    can_delete = True


class AddressAdmin(ModelView):

    can_edit = False
    can_create = True
    can_delete = True


class CheckoutAdmin(ModelView):

    can_edit = True
    can_create = True
    can_delete = True