from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from teleprint_me.blueprints import auth
from teleprint_me.core import product, sqlite
from teleprint_me.forms.strategy import StrategyForm

blueprint = Blueprint("strategy", __name__, url_prefix="/strategy")


@blueprint.route("/menu", methods=("GET",))
@auth.required
def menu():
    return render_template("strategy/menu.html")


@blueprint.route("/read", methods=("GET",))
@auth.required
def read():
    return render_template("strategy/read.html", action="read")


@blueprint.route("/read/<name>", methods=(("GET",)))
@auth.required
def read_one(name):
    return render_template("strategy/read_one.html", name=name)


@blueprint.route("/write/<name>", methods=("GET",))
@auth.required
def write_one(name):
    strategy = sqlite.get_strategy(name)
    if strategy and not list(strategy.datum):
        selection = []
        for row in product.get_rows(g.client, strategy.name):
            data = sqlite.Data(
                date=row.date,
                price=row.price,
                target=row.target,
                value=row.value,
                recommend=row.recommend,
                side=row.side,
                base=row.base,
                base_fee=row.base_fee,
                base_total=row.base_total,
                base_prev=row.base_prev,
                quote=row.quote,
                quote_fee=row.quote_fee,
                quote_total=row.quote_total,
                quote_prev=row.quote_prev,
                period=row.period,
                strategy=strategy,
            )
            if row.period not in ("W", "D"):
                strategy.period = str(row.period)
            selection.append(data)
        with sqlite.database.atomic():
            sqlite.Data.bulk_create(selection, batch_size=50)
        strategy.save()
        flash((("Write", f"Wrote fills to {strategy.name}"),), "info")
    else:
        flash((("Error", f"Failed to write fills using {strategy.name}"),), "error")
    return redirect(url_for("strategy.read_one", name=name))


@blueprint.route("/trade", methods=("GET",))
@auth.required
def trade():
    return render_template("strategy/read.html", action="trade")


@blueprint.route("/trade/<name>", methods=("GET",))
@auth.required
def trade_one(name):
    return render_template("strategy/trade.html", name=name)


@blueprint.route("/delete", methods=("GET",))
@auth.required
def delete():
    return render_template("strategy/read.html", action="delete")


@blueprint.route("/delete/<name>", methods=("GET",))
@auth.required
def delete_one(name):
    try:
        strategy = sqlite.get_strategy(name)
        strategy.delete_instance(recursive=True)
        flash((("Delete", f"Deleted {strategy.name}"),), "info")
    except (AttributeError,):
        flash((("Error", f"{name.upper()} does not exist"),), "error")
    return render_template("strategy/read.html", action="delete", name=name)


@blueprint.route("/create", methods=("GET", "POST"))
@auth.required
def create():
    form = StrategyForm(request.form)
    if request.method == "POST":
        messages = []
        if form.validate_on_submit():
            strategy = sqlite.Strategy.create(
                name=form.name.data.lower(),
                base=form.product.data.split("-")[0].upper(),
                quote=form.product.data.split("-")[1].upper(),
                product=form.product.data.upper(),
                type_=form.type_.data,
                frequency=form.frequency.data,
                principal=f"{form.principal.data:.8f}",
                yield_=f"{form.yield_.data if form.yield_.data else 0}",
                user=g.user,
            )
            strategy.save()
            messages.append(("Create", f"Created {strategy.name}"))
        messages = auth.error(form, messages)
        if messages:
            flash(tuple(messages), "info")
        return redirect(url_for("strategy.create"))
    return render_template("strategy/create.html", form=form)


@blueprint.route("/update/<name>", methods=(("GET",)))
@auth.required
def update(name):
    return render_template("strategy/read.html")
