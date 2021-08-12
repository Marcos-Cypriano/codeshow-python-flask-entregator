from flask import Blueprint, render_template

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/sobre')
def about():
    return render_template('about.html')

@bp.route('/restaurantes')
def restaurants():
    return render_template('restaurants.html')