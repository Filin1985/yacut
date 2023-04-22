from random import choices
from datetime import datetime
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
SHORT_ID_EXISTS = 'Имя "{custom_id}" уже занято.'
CREATE_SHORT_ID_ERROR = 'Не удалось сгенерировать ссылку!'
SHORT_ID_INVALID = "Ссылка должна состоять только из цифр и латинских букв!"
FLASH_SHORT_ID_EXISTS = 'Имя {custom_id} уже занято!'
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

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def create_unique_custom_id():
        for _ in range(GENERATION_NUMBER):
            custom_id = ''.join(choices(
                ALLOWED_SYMBOLS, k=CUSTOM_ID_LENGTH
            ))
            if not URLMap.get_unique_custom_id(custom_id):
                return custom_id
        raise CreatingError(CREATE_SHORT_ID_ERROR)

    @staticmethod
    def validate_custom_id_length(custom_id):
        if len(custom_id) > MAX_CUSTOM_ID_SIZE:
            raise ValidationError(UNACCEPTABLE_URL.format(custom_id=custom_id))
        return custom_id

    @staticmethod
    def validate_custom_id_symbols(custom_id):
        match = re.match(CUSTOM_ID_REGEXP, custom_id)
        if not (match is not None and match.group() == custom_id):
            raise ValidationError(UNACCEPTABLE_URL.format(custom_id=custom_id))
        return custom_id

    @staticmethod
    def get_unique_custom_id(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def validate_url_scheme(original):
        parsed_url = urlparse(original)
        return (parsed_url.scheme and
                parsed_url.netloc)

    @staticmethod
    def validate_url_size(original):
        return len(original) < MAX_ORIGINAL_SIZE

    @staticmethod
    def create_urlmap(
        original, custom_id, existence_message
    ):
        if not custom_id or custom_id == '':
            custom_id = URLMap.create_unique_custom_id()
            print(custom_id)
        if URLMap.get_unique_custom_id(custom_id):
            raise ExistenceError(
                existence_message.format(custom_id=custom_id)
            )
        if (
            custom_id != '' and
            custom_id is not None
        ):
            URLMap.validate_custom_id_symbols(custom_id)
            URLMap.validate_custom_id_length(custom_id)
        if not URLMap.validate_url_scheme(original):
            raise ValidationError(INCORRECT_URL)
        url_object = URLMap(
            original=original,
            short=custom_id
        )
        db.session.add(url_object)
        db.session.commit()
        return url_object
