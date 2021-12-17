from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from peewee import DoesNotExist
from peewee import Model

from teleprint_me.blueprints import auth
from teleprint_me.core import Strategy
from teleprint_me.forms.strategy import StrategyForm

blueprint = Blueprint('strategy', __name__, url_prefix='/strategy')


def get_strategy(name: str) -> Strategy:
    try:
        return Strategy.get(Strategy.name == name)
    except (DoesNotExist,):
        return None


# this needs to be fixed.
# its okay for the prototype tho.
def get_principal(model: Model) -> str:
    if 0 < model.principal < 1:
        return f'{model.principal:.8f}'
    return f'{model.principal:.2f}'


def get_yield(model: Model) -> str:
    if model.yield_:
        return f'{int(model.yield_ * 100)}%'
    return '0%'


def get_type(model: Model) -> str:
    return ' '.join(t.capitalize() for t in model.type_.split('_'))


def get_strategies(models: list[Model]) -> list[dict]:
    data = []
    for model in models:
        data.append({
            'name': model.name.capitalize(),
            'base': model.base,
            'quote': model.quote,
            'product': model.product,
            'type': get_type(model),
            'principal': get_principal(model),
            'frequency': model.frequency.capitalize(),
            'yield': get_yield(model),
            'period': model.period
        })
    return data


@blueprint.route('/menu', methods=('GET',))
@auth.required
def menu():
    return render_template('strategy/menu.html')


@blueprint.route('/read', methods=('GET',))
@auth.required
def read():
    path = 'strategy/read.html'
    action = 'read'
    strategies = get_strategies(g.strategies)
    return render_template(path, action=action, strategies=strategies)


@blueprint.route('/read/<name>', methods=(('GET',)))
@auth.required
def read_one(name):
    path = 'strategy/read_one.html'
    strategy = get_strategy(name)
    return render_template(path, strategy=strategy)


@blueprint.route('/read/write/<name>', methods=('GET',))
@auth.required
def read_write_one(name):
    path = 'strategy/read_one.html'
    strategy = get_strategy(name)
    if strategy:
        flash((('Write', f'Wrote fills to {name}'),), 'info')
    else:
        flash((('Error', f'Failed to write fills to {strategy.name}'),), 'error')
    return render_template(path, strategy=strategy)


@blueprint.route('/trade', methods=('GET',))
@auth.required
def trade():
    path = 'strategy/read.html'
    action = 'trade'
    strategies = get_strategies(g.strategies)
    return render_template(path, action=action, strategies=strategies)


@blueprint.route('/delete', methods=('GET',))
@auth.required
def delete():
    path = 'strategy/read.html'
    action = 'delete'
    strategies = get_strategies(g.strategies)
    return render_template(path, action=action, strategies=strategies)


@blueprint.route('/delete/<name>', methods=('GET',))
@auth.required
def delete_one(name):
    try:
        strategy = get_strategy(name)
        strategy.delete_instance(recursive=True)
        flash((('Delete', f'Deleted {strategy.name}'),), 'info')
    except (AttributeError,):
        flash((('Error', f'{name.upper()} does not exist'),), 'error')
    path = 'strategy/read.html'
    action = 'delete'
    strategies = get_strategies(g.strategies)
    return render_template(path, action=action, strategies=strategies)


@blueprint.route('/create', methods=('GET', 'POST'))
@auth.required
def create():
    form = StrategyForm(request.form)
    if request.method == 'POST':
        messages = []
        if form.validate_on_submit():
            strategy = Strategy.create(
                name=form.name.data.lower(),
                base=form.product.data.split('-')[0].upper(),
                quote=form.product.data.split('-')[1].upper(),
                product=form.product.data.upper(),
                type_=form.type_.data,
                frequency=form.frequency.data,
                principal=form.principal.data,
                yield_=form.yield_.data,
                user=g.user
            )
            strategy.save()
            messages.append(('Create', f'Created {strategy.name}'))
        messages = auth.error(form, messages)
        if messages:
            flash(tuple(messages), 'info')
        return redirect(url_for('strategy.create'))
    return render_template('strategy/create.html', form=form)


@blueprint.route('/update/<name>', methods=(('GET',)))
@auth.required
def update(name):
    strategies = get_strategies(g.strategies)
    return render_template('strategy/read.html', strategies=strategies)
