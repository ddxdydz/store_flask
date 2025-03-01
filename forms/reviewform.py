from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, SelectField, FileField, BooleanField
from wtforms.fields.simple import TextAreaField


class ReviewForm(FlaskForm):
    profile_img = FileField(
        'Изменить фото отзыва', validators=[
            FileAllowed(['jpg', 'png'])])
    delete_img = BooleanField('Удалить текущее фото после подтверждения изменений?')
    about = TextAreaField('Текст отзыва')
    score = SelectField(u'Оценка', choices=[
        (str(i), str(i)) for i in range(0, 6)])
    submit = SubmitField('Подтвердить')
