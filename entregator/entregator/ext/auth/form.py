import wtforms as wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class UserForm(FlaskForm):
    email = wtf.StringField('Email', [wtf.validators.DataRequired(), wtf.validators.Email()])
    passwd = wtf.PasswordField('Senha', [wtf.validators.DataRequired()])
    foto = FileField('Foto')

class OrderForm(FlaskForm):
    #O QUE PREENCHER NSAS FUNÇÕES ABAIXO
    #ADICIONAR UM ESPAÇO PARA OS ITENS DO PEDIDO
    created_at = wtf.DateTimeField()
    completed = wtf.BooleanField()
    user_id = wtf.IntegerField()
    store_id = wtf.IntegerField()
    address_id = wtf.IntegerField()

class OrderItemsForm(FlaskForm):
    order_id = wtf.IntegerField()
    items_id = wtf.IntegerField()
    quant = wtf.IntegerField()

class CheckoutForm(FlaskForm):
    payment = wtf.StringField()
    total = wtf.FloatField()
    created_at = wtf.DateTimeField()
    completed = wtf.BooleanField()
    order_id = wtf.IntegerField()
