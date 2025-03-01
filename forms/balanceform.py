from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import NumberRange, DataRequired


class BalanceForm(FlaskForm):
    count = IntegerField(
        'Введите сумму пополнения',
        default=0, validators=[DataRequired(), NumberRange(
            min=1, max=10000, message='Число должно быть в диапазоне от 1 до 10000')]
    )
    about = StringField('Введите дополнительные данные для пополнения')
    submit = SubmitField('Подтвердить')
