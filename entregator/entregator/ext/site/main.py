from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash


from entregator.ext.auth.form import OrderItemsForm, UserForm, AddressForm
from entregator.ext.db.models import Address, Category, Checkout, Items, Order, Store, User
from entregator.ext.site.controllers import cart_params, evaluate_items_order, evaluate_order
from entregator.ext.auth.controller import add_address, alter_address_order, complete_order, create_checkout, create_user, delete_address, delete_order_items, save_user_photo, create_order

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
        return redirect(url_for('site.index'))

    '''if request.method == 'POST':
        __import__('ipdb').set_trace()'''

    return render_template('userform.html', form=form, categories=categories)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    categories = Category.query.all()
    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and (check_password_hash(user.passwd, form.passwd.data) or user.passwd == form.passwd.data):#RETIRAR ANTES DO DEPLOY
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
        enderecos = current_user.addresses.all()
        pedidos = current_user.orders.filter_by(completed=1).all()
        if pedidos:
            lista = []
            for pedido in pedidos:
                check = pedido.checkout.first()
                items_list, tot = cart_params(pedido)
                lista.append({'items': items_list, 'total': tot, 'restaurante': pedido.store, 'situacao': check.completed})

            return render_template('profile.html', enderecos=enderecos, lista=lista, categories=categories)
        else:
            return render_template('profile.html', enderecos=enderecos, categories=categories)
            
    else:
        flash('Você precisa estar logado para acessar um perfil!', 'error')
        return redirect(url_for('site.login'))
      

@bp.route('/endereco', methods=['GET', 'POST'])
def address():
        categories = Category.query.all()

        form = AddressForm()

        if form.validate_on_submit():
            add_address(zip=form.zip.data, country=form.country.data, address=form.address.data, user_id=current_user.id)
            flash('Endereço cadastrado com sucesso!', 'info')
            return redirect(url_for('site.profile'))
        else:
            return render_template('address.html', form=form, categories=categories)


@bp.route('/remover_endereco/<endereco>', methods=['GET', 'DELETE'])
def remove_address(endereco):
    frase = delete_address(endereco)
    flash(frase)
    return redirect(url_for('site.profile'))
         
 

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logout com sucesso!', 'info')
    return redirect(url_for('site.index'))


@bp.route('/pesquisa', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        pesquisa = str(request.form['search'])
        results_r = Store.query.search(pesquisa, or_=True)
        results_c = Items.query.search(pesquisa, or_=True)

        if 'null' in str(results_c) and 'null' in str(results_r):
            flash('Nenhum restaurante ou prato foi encontrado', 'error')
            return redirect(url_for('site.index'))
        elif 'null' in str(results_c):
            return render_template('search.html', restaurants=results_r)
        elif 'null' in str(results_r):
            return render_template('search.html', foods=results_c)
        else:
            return render_template('search.html', restaurants=results_r, foods=results_c)
    
    return redirect(url_for('site.index'))

@bp.route('/restaurantes')
def restaurants():
    categories = Category.query.all()
    stores = Store.query.filter_by(active=True).all()

    return render_template('restaurants.html', categories=categories, stores=stores)


@bp.route('/restaurantes/<categoria>')
def category_restaurants(categoria):
    categories = Category.query.all()

    category = Category.query.filter_by(name=categoria).first()
    stores = category.stores.filter_by(active=True).all()

    return render_template('category_restaurants.html', categories=categories, stores=stores)


@bp.route('/restaurante/<loja>', methods=['GET'])
def page_restaurant(loja):
    categories = Category.query.all()

    estabelecimento = Store.query.filter_by(id=loja).first()

    itens = estabelecimento.items.filter_by(available=True).all()

    return render_template('page_restaurant.html', categories=categories, foods=itens, loja=estabelecimento.name)


@bp.route('/comida/<item>', methods=['GET', 'POST'])
def page_item(item):
    categories = Category.query.all()
    comida = Items.query.filter_by(id=item).first()
    estabelecimento = comida.store

    if current_user.is_active:
        form = OrderItemsForm()

        if form.validate_on_submit():
            if form.quant.data == None or form.quant.data == 0:
                flash('Você precisa adicionar uma quantidade ao prato escolhido!', 'error')
                return redirect(url_for('site.page_item', item=item))
            else:
                order = current_user.orders.order_by(Order.id.desc()).first()

                if order == None or order.completed or order.expired: 
                    order = create_order(user_id=current_user.id, store_id=estabelecimento.id)

                aviso = evaluate_order(loja=estabelecimento.id, order=order)
                if aviso:
                    flash(aviso, 'error')
                    return redirect(url_for('site.cart'))

                evaluate_items_order(quantidade=form.quant.data, order=order, comida=item)
                return redirect(url_for('site.cart'))

        return render_template('/page_item.html', categories=categories, foods=comida, form=form, loja=estabelecimento.name)
    else:
        flash('Cadastre-se ou entre na sua conta para começar um pedido!', 'error')
        return redirect(url_for('site.login'))


@bp.route('/meu-carrinho', methods=['GET', 'POST'])
def cart():
    categories = Category.query.all()

    order = current_user.orders.order_by(Order.id.desc()).first()
    enderecos = current_user.addresses
    loja = order.store

    if order == None or order.completed or order.expired:
        flash('Não há um pedido aberto.', 'error')
        return redirect(url_for('site.index'))
    else:
        items_list, tot = cart_params(order)


    return render_template('/cart.html', categories=categories, order=order, order_items=items_list, tot=tot, enderecos=enderecos, loja=loja)


@bp.route('/remover/<item>', methods=['GET', 'DELETE'])
def remove(item):
    frase = delete_order_items(item)
    flash(frase)

    return redirect(url_for('site.cart'))


@bp.route('/confirmado/<order>', methods=['GET', 'POST'])
def checkout(order):
    endereco = request.form.get('endereco')
    try:
        alter_address_order(id=order, address_id=endereco)
        complete_order(order_id=order, completed=True)
    except:
        flash('Pedido não pode ser confirmado!', 'error')
        return render_template('/checkout.html')

    value = request.form.get('pagamento')
    # add = Address.query.filter_by(id=endereco).first()
    add = Address.query.get(endereco)

    # pedido = Order.query.filter_by(id=order).first()
    pedido = Order.query.get(order)
    # loja = Store.query.filter_by(id=pedido.store_id).first()
    loja = pedido.store
    items_list, tot = cart_params(pedido)
    
    checkout = create_checkout(order=pedido, payment=value)
    
    flash('Pedido confirmado! Aguarde mais informações diretamente do restaurante.', 'info')
    return render_template('/checkout.html', loja=loja.name, items_list=items_list, tot=checkout.total, pag=checkout.payment, endereco=add)
