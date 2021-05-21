import flask


app = flask.Flask(__name__)


@app.route('/')
def index():
    flask.url_for('static', filename='main.css')
    return 'index'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        flask.url_for('index')
    return 'register'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.url_for('index')
    return 'login'


@app.route('/logout')
def logout():
    return 'logout'
