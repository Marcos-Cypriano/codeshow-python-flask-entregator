from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user

from entregator.ext.auth.form import CheckoutForm, OrderItemsForm, UserForm
from entregator.ext.db.models import Address, Category, Items, Order, OrderItems, Store, User
from entregator.ext.auth.controller import alter_order, complete_order, create_checkout, create_order_items, create_order, create_user, delete_order_items, save_user_photo 

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    categories = Category.query.all()
    stores = Store.query.filter(Store.id < 5)

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

    estabelecimento = Store.query.filter_by(name=loja).first()

    itens = Items.query.filter_by(store_id=estabelecimento.id).all()

    return render_template('page_restaurant.html', categories=categories, stores=itens, loja=loja)


@bp.route('/meu-carrinho/<loja>/<item>', methods=['GET', 'POST'])
def cart_order(loja, item):
    categories = Category.query.all()

    if not current_user.is_active:
        flash('Você precisa estar logado para adicionar uma comida ao carrinho!')
        return redirect('/login')

    else:
        #Informações para criar o Order
        endereco = Address.query.filter_by(user_id=current_user.id).first()

        order = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).first()

        if order == None or order.completed: 
            order = create_order(user_id=current_user.id, store_id=loja, address_id=endereco.id)
        else:
            if int(loja) != order.store_id:
                ordered_items = OrderItems.query.filter_by(order_id=order.id).all()

                if ordered_items:
                    flash('O seu pedido deve ser todo apenas de uma loja!')
                    return redirect('/')
                else:
                    alter_order(id=order.id, store_id=loja)

        comida = Items.query.filter_by(id=item).first()
        
        #Formulário do OrderItems
        form = OrderItemsForm()

        if form.validate_on_submit():
            create_order_items(order_id=order.id, items_id=comida.id, quant=form.quant.data)

            order_items = OrderItems.query.filter_by(order_id=order.id).all()
            items_list = []
            for it in order_items:
                prato = Items.query.filter_by(id=it.items_id).first()
                items_list.append({'name': prato.name, 'quantidade': it.quant, 'preco': prato.price, 'id': it.id})

            return render_template('/cart.html', categories=categories, order=order, order_items=items_list)

    return render_template('cart_order.html', categories=categories, form=form, comida=comida, item=item, loja=loja)


@bp.route('/meu-carrinho', methods=['GET', 'POST'])
def cart():
    categories = Category.query.all()

    order = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).first()

    if order.completed:
        flash('Não há um pedido aberto.')
        return redirect('/')
    else:
        order_items = OrderItems.query.filter_by(order_id=order.id).all()
        items_list = []
        tot = 0
        for item in order_items:
            prato = Items.query.filter_by(id=item.items_id).first()
            items_list.append({'name': prato.name, 'quantidade': item.quant, 'preco': prato.price, 'id': item.id})
            tot += prato.price * item.quant

    return render_template('/cart.html', categories=categories, order=order, order_items=items_list, tot=tot)


@bp.route('/remover/<item>', methods=['GET', 'POST'])
def remove(item):
    frase = delete_order_items(item)

    # order_items = OrderItems.query.filter_by(order_id=order.id).all()
    # items_list = []
    # for it in order_items:
    #     prato = Items.query.filter_by(id=it.items_id).first()
    #     items_list.append({'name': prato.name, 'quantidade': it.quant, 'preco': prato.price})
    flash(frase)

    return redirect('/')


@bp.route('/confirmado/<order>', methods=['GET', 'POST'])
def checkout(order):
    try:
        complete_order(order_id=order, completed=True)
    except:
        flash('Pedido não pode ser confirmado!')
        return render_template('/checkout.html')

    value = request.form.get('pagamento')

    pedido = Order.query.filter_by(id=order).first()
    loja = Store.query.filter_by(id=pedido.store_id).first()
    pratos = OrderItems.query.filter_by(order_id=order).all()
    items_list = []

    for item in pratos:
            prato = Items.query.filter_by(id=item.items_id).first()
            items_list.append({'name': prato.name, 'quantidade': item.quant, 'preco': prato.price, 'id': item.id})

    
    checkout = create_checkout(payment=value, order_id=order)
    
    flash('Pedido confirmado! Aguarde mais informações diretamente do restaurante.')
    return render_template('/checkout.html', loja=loja.name, items_list=items_list, tot=checkout.total, pag=checkout.payment)

    
