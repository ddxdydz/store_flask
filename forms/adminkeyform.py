from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class AdminKeyForm(FlaskForm):
    admin_key = StringField('Введите admin_key')
    submit = SubmitField('Подтвердить')
