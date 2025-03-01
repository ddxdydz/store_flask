from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class OrderSubmitForm(FlaskForm):
    address = StringField('Введите место доставки', validators=[DataRequired()])
    comment = StringField('Введите комментарий к заказу')
    submit = SubmitField('Подтвердить')
