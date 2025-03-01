from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from db.petstore_init_data.init_basic_data import CATEGORIES

choices = [(str(0), "ВСЕ")] + [(str(i + 1), CATEGORIES[i]) for i in range(len(CATEGORIES))]


class ProductSearchForm(FlaskForm):
    search = StringField('Поиск:')
    category = SelectField('Категория', choices=choices)
    submit = SubmitField('Найти')
