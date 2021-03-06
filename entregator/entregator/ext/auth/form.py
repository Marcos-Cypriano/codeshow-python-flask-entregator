import wtforms as wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class UserForm(FlaskForm):
    email = wtf.StringField('Email', [wtf.validators.DataRequired(), wtf.validators.Email()])
    passwd = wtf.PasswordField('Senha', [wtf.validators.DataRequired()])
    foto = FileField('Foto')

class AddressForm(FlaskForm):
    zip = wtf.StringField("Zip Code", [wtf.validators.Length(3,45)])
    country = wtf.StringField()
    address = wtf.StringField("Address", [wtf.validators.Length(min=5)])

class OrderForm(FlaskForm):
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
