# teleprint_me/forms/contact.py
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        description="email",
        name="email",
        render_kw={"placeholder": "email"},
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired()],
        description="subject",
        name="subject",
        render_kw={"placeholder": "subject"},
    )
    body = TextAreaField(
        "Message",
        validators=[DataRequired()],
        description="body",
        name="body",
        render_kw={"placeholder": "message body"},
    )
    submit = SubmitField("Send")
