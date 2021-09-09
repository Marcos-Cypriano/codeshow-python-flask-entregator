from flask import Blueprint, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import login_user, logout_user

from entregator.ext.auth.form import UserForm
from entregator.ext.db.models import Category, Items, Store, User
from entregator.ext.auth.controller import create_user, save_user_photo 

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    categories = Category.query.all()
    stores = Store.query.filter(Store.id < 4)

    return render_template('index.html', categories=categories, stores=stores)

@bp.route('/sobre')
def about():
    categories = Category.query.all()
    return render_template('about.html', categories=categories)

@bp.route('/cadastro', methods=['GET', 'POST'])
def signup():
    categories = Category.query.all()

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

    return render_template('userform.html', form=form, categories=categories)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    categories = Category.query.all()

    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.passwd == form.passwd.data:
            login_user(user)
            flash('Login com sucesso!')
            return redirect(url_for('site.index'))
        else:
            flash('Usuário ou senha incorretos!')

    return render_template('login.html', form = form, categories=categories)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logout com sucesso!')
    return redirect(url_for('site.index'))

@bp.route('/restaurantes')
def restaurants():
    categories = Category.query.all()
    stores = Store.query.all()

    return render_template('restaurants.html', categories=categories, stores=stores)

@bp.route('/restaurantes/<categoria>')
def category_restaurants(categoria):
    categories = Category.query.all()

    restaurantes = Category.query.filter_by(name=categoria).first()

    stores = Store.query.filter_by(category_id=restaurantes.id)

    return render_template('category_restaurants.html', categories=categories, stores=stores)

@bp.route('/restaurante/<loja>')
def page_restaurant(loja):
    categories = Category.query.all()

    store = Store.query.filter_by(name=loja).first()

    itens = Items.query.filter_by(store_id=store.id).all()

    return render_template('page_restaurant.html', categories=categories, stores=itens)