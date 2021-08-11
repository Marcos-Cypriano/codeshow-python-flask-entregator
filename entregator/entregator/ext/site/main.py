from flask import Blueprint, render_template, request

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template(
        'index.html', 
        name=request.args['name']
        )