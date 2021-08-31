from flask import Blueprint, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import login_user, logout_user

from entregator.ext.auth.form import UserForm
from entregator.ext.db.models import User
from entregator.ext.auth.controller import create_user, save_user_photo 

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/sobre')
def about():
    return render_template('about.html')

@bp.route('/cadastro', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if form.validate_on_submit():
        create_user(email=form.email.data, passwd=form.passwd.data)

        foto = request.files.get('foto')
        if foto:
            save_user_photo(foto.filename, foto)
        #Forçar o Login
        return redirect('/')

    '''if request.method == 'POST':
        __import__('ipdb').set_trace()'''

    return render_template('userform.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.passwd == form.passwd.data:
            login_user(user)
            flash('Login com sucesso!')
            return redirect(url_for('site.index'))
        else:
            flash('Usuário ou senha incorretos!')

    return render_template('login.html', form = form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logout com sucesso!')
    return redirect(url_for('site.index'))

@bp.route('/restaurantes')
def restaurants():
    return render_template('restaurants.html')