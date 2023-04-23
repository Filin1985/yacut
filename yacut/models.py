from datetime import datetime
from random import choices
import re
from urllib.parse import urlparse

from flask import url_for

from settings import (
    GENERATION_NUMBER,
    MAX_CUSTOM_ID_SIZE,
    MAX_ORIGINAL_SIZE,
    CUSTOM_ID_LENGTH,
    CUSTOM_ID_REGEXP,
    ALLOWED_SYMBOLS,
    REDIRECT_FUNCTION
)
from . import db
from .error_handlers import CreatingError, ExistenceError, ValidationError


UNACCEPTABLE_URL = 'Указано недопустимое имя для короткой ссылки'
CREATE_CUSTOM_ID_ERROR = 'Не удалось сгенерировать ссылку!'
FLASH_CUSTOM_ID_EXISTS = 'Имя {custom_id} уже занято!'
INCORRECT_URL = 'Введите корректный URL адрес'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_SIZE), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_SIZE), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_FUNCTION, short_url=self.short, _external=True
            )
        )

    @staticmethod
    def create_unique_custom_id():
        for _ in range(GENERATION_NUMBER):
            custom_id = ''.join(choices(
                ALLOWED_SYMBOLS, k=CUSTOM_ID_LENGTH
            ))
            if not URLMap.get_urlmap_item(custom_id):
                return custom_id
        raise CreatingError(CREATE_CUSTOM_ID_ERROR)

    @staticmethod
    def get_urlmap_item(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def create_urlmap(
        original, custom_id, validation=False
    ):
        if validation:
            if (
                custom_id != '' and
                custom_id is not None
            ):
                if len(custom_id) > MAX_CUSTOM_ID_SIZE:
                    raise ValidationError(
                        UNACCEPTABLE_URL.format(custom_id=custom_id)
                    )
                if not re.match(CUSTOM_ID_REGEXP, custom_id):
                    raise ValidationError(
                        UNACCEPTABLE_URL.format(custom_id=custom_id)
                    )
        custom_id = custom_id or URLMap.create_unique_custom_id()
        if URLMap.get_urlmap_item(custom_id):
            raise ExistenceError(
                FLASH_CUSTOM_ID_EXISTS.format(custom_id=custom_id)
            )
        if validation:
            if len(original) > MAX_ORIGINAL_SIZE:
                raise ValidationError(INCORRECT_URL)
            parsed_url = urlparse(original)
            if not (parsed_url.scheme and parsed_url.netloc):
                raise ValidationError(INCORRECT_URL)
        urlmap_object = URLMap(
            original=original,
            short=custom_id
        )
        db.session.add(urlmap_object)
        db.session.commit()
        return urlmap_object
