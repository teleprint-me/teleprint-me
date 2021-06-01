from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from bson.objectid import ObjectId

from ledger.core.extensions import mongo
from ledger import auth

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@auth.required
def index():
    if request.method == 'POST':
        flash(('Message', 'This is the root response'))
    flash(('Session', f'Signed in as {g.user["email"]}'))
    return render_template('index.html')
