from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional, DataRequired, URL

from settings import MAX_ORIGINAL_SIZE, MAX_SHORT_ID_SIZE


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Введите корректный адресс ссылки'),
                    Length(max=MAX_ORIGINAL_SIZE)]
    )
    custom_id = URLField(
        'Введите ваш вариант короткой ссылки',
        validators=[Length(max=MAX_SHORT_ID_SIZE),
                    Optional()]
    )
    submit = SubmitField('Создать')
