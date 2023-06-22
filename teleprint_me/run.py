# teleprint_me/run.py
import smtplib
from email.message import EmailMessage
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, send_from_directory, url_for

from teleprint_me.forms.contact import ContactForm
from teleprint_me.static import static_path

app = Flask(
    __name__,
    static_folder=static_path.directory,
    template_folder=static_path.get("views"),
)

app.config["SECRET_KEY"] = str(uuid4())  # Replace with your actual secret key


#
# Static Content
#
@app.route("/static/<path:filepath>")
def serve_static(filepath):
    return send_from_directory(static_path.directory, filepath)


#
# Dynamic Content
#
@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        msg = EmailMessage()
        msg["From"] = form.email.data
        msg["Subject"] = form.subject.data
        msg["To"] = "your_email@example.com"
        msg.set_content(form.body.data)

        try:
            with smtplib.SMTP("localhost") as s:
                # If your SMTP server requires authentication, you'll need to call
                # s.login(user, password) before calling s.send_message(msg).
                s.send_message(msg)
            flash("Your message has been sent successfully.", "success")
        except Exception as e:
            flash(f"There was an error sending your message: {e}.", "error")
        return redirect(url_for("index"))
    return render_template("index.html", form=form)


# development settings are not to be used in production
if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
