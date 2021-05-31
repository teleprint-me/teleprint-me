from flask import Blueprint
from flask import request

from ledger import auth

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@auth.required
def index():
    if request.method == 'POST':
        return 'This is the root response!'
    return 'Hello, World!'
