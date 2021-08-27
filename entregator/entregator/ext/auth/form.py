import wtforms as wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class UserForm(FlaskForm):
    email = wtf.StringField('Email', [wtf.validators.DataRequired(), wtf.validators.Email()])
    passwd = wtf.PasswordField('Senha', [wtf.validators.DataRequired()])
    foto = FileField('Foto')

#ADICIONAR o FLask-login para o usuário fazer login