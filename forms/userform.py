from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, \
    SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    profile_img = FileField(
        'Изменить фото профиля', validators=[
            FileAllowed(['jpg', 'png'])])
    delete_img = BooleanField('Удалить текущее фото после подтверждения изменений?')
    about = TextAreaField('Описание')
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')
