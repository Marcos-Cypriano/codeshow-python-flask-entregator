from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, current_user


from entregator.ext.auth.form import OrderItemsForm, UserForm, AddressForm
from entregator.ext.db.models import Address, Category, Items, Order, Store, User
from entregator.ext.site.controllers import cart_params, evaluate_items_order, evaluate_order
from entregator.ext.auth.controller import add_address, complete_order, create_checkout, create_user, delete_order_items, save_user_photo 

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
        user = create_user(email=form.email.data, passwd=form.passwd.data)

        foto = request.files.get('foto')
        if foto:
            save_user_photo(foto.filename, foto)
        
        login_user(user)
        flash('Usuário cadastrado com sucesso! Não se esqueça de cadastrar um enredeço.', 'info')
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
            flash('Login com sucesso!', 'info')
            return redirect(url_for('site.index'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html', form = form, categories=categories)

@bp.route('/perfil')
def profile():
    categories = Category.query.all()

    if current_user.is_active:
        enderecos = Address.query.filter_by(user_id=current_user.id).all()
        pedidos = Order.query.filter_by(user_id=current_user.id, completed=1, expired=0).all()
        if pedidos:
            lista = []
            for pedido in pedidos:
                items_list, tot = cart_params(pedido.id)
                lista.append({'items': items_list, 'total': tot, 'restaurante': pedido.store})

                return render_template('profile.html', enderecos=enderecos, lista=lista, categories=categories)
        else:
            return render_template('profile.html', enderecos=enderecos, categories=categories)
            
    else:
        flash('Você precisa estar logado para acessar um perfil!', 'error')
        return redirect('/login')
      

@bp.route('/endereco', methods=['GET', 'POST'])
def address():
        categories = Category.query.all()

        form = AddressForm()

        if form.validate_on_submit():
            add_address(zip=form.zip.data, country=form.country.data, address=form.address.data, user_id=current_user.id)
            flash('Endereço cadastrado com sucesso!', 'info')
            return redirect('/perfil')
        else:
            return render_template('address.html', form = form, categories=categories)
         
 

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logout com sucesso!', 'info')
    return redirect(url_for('site.index'))


@bp.route('/restaurantes')
def restaurants():
    categories = Category.query.all()
    stores = Store.query.filter_by(active=True).all()

    return render_template('restaurants.html', categories=categories, stores=stores)


@bp.route('/restaurantes/<categoria>')
def category_restaurants(categoria):
    categories = Category.query.all()

    restaurantes = Category.query.filter_by(name=categoria).first()

    stores = Store.query.filter_by(category_id=restaurantes.id, active=True).all()

    return render_template('category_restaurants.html', categories=categories, stores=stores)


@bp.route('/restaurante/<loja>')
def page_restaurant(loja):
    categories = Category.query.all()

    estabelecimento = Store.query.filter_by(name=loja).first()

    itens = Items.query.filter_by(store_id=estabelecimento.id, available=True).all()

    return render_template('page_restaurant.html', categories=categories, stores=itens, loja=estabelecimento.name)


@bp.route('/meu-carrinho/<loja>/<item>', methods=['GET', 'POST'])
def cart_order(loja, item):
    categories = Category.query.all()

    if not current_user.is_active:
        flash('Você precisa estar logado para adicionar uma comida ao carrinho!', 'error')
        return redirect('/login')
    else:
        if not Address.query.filter_by(user_id=current_user.id).first():
            flash('Você precisa cadastrar um endereço antes de pedir.', 'error')
            return redirect('/address')

        order = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).first()

        aviso = evaluate_order(loja=loja, order=order, user=current_user.id)
        if aviso:
            flash(aviso)
            return redirect('/')

        comida = Items.query.filter_by(id=item).first()
        
        form = OrderItemsForm()
        if form.validate_on_submit():
            items_list, tot= evaluate_items_order(quantidade=form.quant.data,item=item, order_id=order.id, comida=comida)
            return render_template('/cart.html', categories=categories, order=order, order_items=items_list, tot=tot)

    return render_template('cart_order.html', categories=categories, form=form, comida=comida, item=item, loja=loja)


@bp.route('/meu-carrinho', methods=['GET', 'POST'])
def cart():
    categories = Category.query.all()

    order = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).first()

    if order == None or order.completed or order.expired:
        flash('Não há um pedido aberto.', 'error')
        return redirect('/')
    else:
        items_list, tot = cart_params(order.id)

    return render_template('/cart.html', categories=categories, order=order, order_items=items_list, tot=tot)


@bp.route('/remover/<item>', methods=['GET', 'DELETE'])
def remove(item):
    frase = delete_order_items(item)
    flash(frase)

    return redirect('/')


@bp.route('/confirmado/<order>', methods=['GET', 'POST'])
def checkout(order):
    try:
        complete_order(order_id=order, completed=True)
    except:
        flash('Pedido não pode ser confirmado!', 'error')
        return render_template('/checkout.html')

    value = request.form.get('pagamento')

    pedido = Order.query.filter_by(id=order).first()
    loja = Store.query.filter_by(id=pedido.store_id).first()
    items_list, tot = cart_params(order_id=pedido.id)
    
    checkout = create_checkout(payment=value, order_id=order)
    
    flash('Pedido confirmado! Aguarde mais informações diretamente do restaurante.', 'info')
    return render_template('/checkout.html', loja=loja.name, items_list=items_list, tot=checkout.total, pag=checkout.payment)
