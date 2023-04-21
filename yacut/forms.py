from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional, DataRequired, URL, Regexp

from settings import MAX_ORIGINAL_SIZE, MAX_SHORT_ID_SIZE, SHORT_ID_REGEXP


LINK_HINT = 'Введите ссылку'
LINK_REQUIRED = 'Обязательное поле'
LINK_INCORRECT = 'Введите корректный адресс ссылки'
SHORT_LINK_HINT = 'Введите ваш вариант короткой ссылки'
SUBMIT_HINT = 'Создать'
REGEXP_MESSAGE = 'Допустимы только цифры и латинские буквы'


class URLForm(FlaskForm):
    original_link = URLField(
        LINK_HINT,
        validators=[DataRequired(message=LINK_REQUIRED),
                    URL(message=LINK_INCORRECT),
                    Length(max=MAX_ORIGINAL_SIZE)]
    )
    custom_id = URLField(
        SHORT_LINK_HINT,
        validators=[Length(max=MAX_SHORT_ID_SIZE),
                    Optional(),
                    Regexp(regex=SHORT_ID_REGEXP, message=REGEXP_MESSAGE)]
    )
    submit = SubmitField(SUBMIT_HINT)
