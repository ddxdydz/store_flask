from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import IntegerField, SubmitField, StringField, SelectField, FileField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

from db.petstore_init_data.init_basic_data import CATEGORIES
from forms.validators.FileSizeValidator import FileSizeValidator


class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    category = SelectField(u'Категория', choices=[
        (str(i + 1), CATEGORIES[i]) for i in range(len(CATEGORIES))])
    long_description = TextAreaField('Длинное описание')
    short_description = StringField('Короткое описание')
    specifications = TextAreaField('Характеристики')
    price = IntegerField('Цена', default=1000)
    promo = StringField('Акция')
    profile_img = FileField(
        'Изменить фото товара', validators=[
            FileAllowed(['.jpg', '.png']), FileSizeValidator()])
    delete_img = BooleanField('Удалить текущее фото после подтверждения изменений?')

    submit = SubmitField('Подтвердить')

    error_price_message = "Ошибка ввода: Цена товара должна быть числом в диапазоне от 1 до 999999999"
