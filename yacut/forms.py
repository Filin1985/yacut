from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional, DataRequired, Regexp

class URLForm(FlaskForm):
    original_link  = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = URLField(
        'Введите ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')