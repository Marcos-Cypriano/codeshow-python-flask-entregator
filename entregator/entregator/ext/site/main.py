from flask import Blueprint, render_template, redirect, request
from entregator.ext.auth.form import UserForm
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

@bp.route('/restaurantes')
def restaurants():
    return render_template('restaurants.html')