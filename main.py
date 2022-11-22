from bottle import Bottle, static_file, run
from teleprint_me.static import static_path, module_path


app = Bottle()


#
# Static Content
#
@app.route("/images/<filepath:path>")
def images(filepath):
    return static_file(filepath, root=static_path.images)


@app.route("/styles/<filepath:path>")
def styles(filepath):
    return static_file(filepath, root=static_path.styles)


@app.route("/scripts/<filepath:path>")
def scripts(filepath):
    return static_file(filepath, root=static_path.scripts)


@app.route("/grassroots/<filepath:path>")
def grassroots(filepath):
    return static_file(filepath, root=module_path.grassroots)


#
# Dynamic Content
#
@app.route("/")
def root():
    return static_file("index.html", root=static_path.views)


@app.route("/profile")
def view_profile():
    return static_file("profile.html", root=static_path.views)


@app.route("/portfolio")
def view_portfolio():
    return static_file("portfolio.html", root=static_path.views)


@app.route("/contact")
def view_contact():
    return static_file("contact.html", root=static_path.views)


# these settings are not to be used in production
run(app, host="localhost", port=8080, reloader=True, debug=True)
