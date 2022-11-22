from bottle import Bottle, static_file, run
from teleprint_me.static import static_path, module_path


app = Bottle()


#
# Static Content
#
@app.route("/static/<filepath:path>")
def static(filepath):
    return static_file(filepath, root=static_path.directory)


@app.route("/modules/<filepath:path>")
def modules(filepath):
    return static_file(filepath, root=module_path.directory)


#
# Dynamic Content
#
@app.route("/")
def index():
    return static_file("index.html", root=static_path.get("views"))


@app.route("/profile")
def view_profile():
    return static_file("profile.html", root=static_path.get("views"))


@app.route("/portfolio")
def view_portfolio():
    return static_file("portfolio.html", root=static_path.get("views"))


@app.route("/contact")
def view_contact():
    return static_file("contact.html", root=static_path.get("views"))


# development settings are not to be used in production
run(app, host="localhost", port=8080, reloader=True, debug=True)
