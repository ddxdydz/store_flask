from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from db.petstore_init_data.init_basic_data import ROLES

choices = [(str(0), "ВСЕ")] + [(str(i + 1), ROLES[i]) for i in range(len(ROLES))]


class UserSearchForm(FlaskForm):
    search = StringField('Поиск:')
    role = SelectField('Роль', choices=choices)
    submit = SubmitField('Найти')
