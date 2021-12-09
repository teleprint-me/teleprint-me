from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from peewee import DoesNotExist

from teleprint_me.blueprints import auth
from teleprint_me.core import Strategy
from teleprint_me.forms.strategy import StrategyForm

blueprint = Blueprint('strategy', __name__, url_prefix='/strategy')


def get_strategy(name: str) -> Strategy:
    try:
        return Strategy.get(Strategy.name == name)
    except (DoesNotExist,):
        return None


@blueprint.route('/menu', methods=('GET',))
@auth.required
def menu():
    return render_template('strategy/menu.html')


@blueprint.route("/create", methods=('GET', 'POST'))
@auth.required
def create():
    form = StrategyForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            strategy = Strategy.create(
                name=form.name.data,
                product=form.product.data,
                type_=form.type_.data,
                principal=form.principal.data,
                frequency=form.frequency.data,
                yield_=form.yield_.data,
                user=g.user
            )
            strategy.save()
            messages.append(('Create', f'Created {strategy.name}'))
        for key, value in form.errors.items():
            try:
                messages.append((key, value[0]))
            except (IndexError,) as e:
                messages.append(('Error', e))
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('strategy.create'))
    return render_template('strategy/create.html', form=form)


@blueprint.route('/read', methods=(('GET',)))
@auth.required
def read():
    return render_template('strategy/read.html')


@blueprint.route('/delete', methods=('GET', 'POST'))
@auth.required
def delete():
    name = request.args.get('name')
    strategy = get_strategy(name)
    if name and strategy:
        strategy.delete_instance()
        messages = [('Delete', f'Deleted {strategy.name}')]
        flash(tuple(messages), 'info')
        return redirect(url_for('strategy.delete'))
    return render_template('strategy/delete.html')


@blueprint.route('/trade', methods=('GET', 'POST'))
@auth.required
def trade():
    context = [{'platform': client.name, 'assets': client.get_assets()} for client in g.clients]
    products = [product for product in g.db.assets.find()]
    if request.method == "POST":
        pass
    return render_template('strategy/trade.html', context=context, assets=products)


@blueprint.route('/trade/<product>', methods=('GET', 'POST'))
@auth.required
def trade_product(product):
    if request.method == 'POST':
        pass
    return {'asset', product}
