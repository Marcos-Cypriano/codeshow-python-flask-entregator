import os
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app as app
from entregator.ext.db.models import User
from entregator.ext.db import db


ALG = 'pbkdf2:sha256'
#Mudar para o Models
def create_user(email: str, passwd: str, admin: bool=False) -> User:
    user = User(email=email, passwd=generate_password_hash(passwd, ALG), admin=admin)
    db.session.add(user)
    #TRATAR exceção caso o usuário já exista!
    db.session.commit()
    return user

def save_user_photo(filename, filestorage):
    '''Saves user photo in .uploads/user/dfhioadihow.ext'''
    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    #VERIFICAR se o diretório existe; criar caso não exista
    filestorage.save(filename)