from datetime import datetime
from urllib.parse import urlparse
from random import choices
import re
from string import ascii_letters, digits

from flask import url_for

from settings import (
    GENERATION_NUMBER,
    MAX_SHORT_ID_SIZE,
    MAX_ORIGINAL_SIZE,
    SHORT_LENGTH,
    SHORT_ID_REGEXP
)
from . import db
from .error_handlers import CreatingError, ExistenceError, ValidationError


UNACCEPTABLE_URL = 'Указано недопустимое имя для короткой ссылки'
ALLOWED_SYMBOLS = ascii_letters + digits
SHORT_ID_EXISTS = 'Имя "{custom_id}" уже занято.'
REDIRECT_FUNCTION = 'redirect_to_original'
CREATE_SHORT_ID_ERROR = 'Не удалось сгенерировать ссылку!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_SIZE), nullable=False)
    short = db.Column(db.String(MAX_SHORT_ID_SIZE), unique=True)
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
    def get_unique_short_id():
        for _ in range(GENERATION_NUMBER):
            short_id = ''.join(choices(
                ALLOWED_SYMBOLS, k=SHORT_LENGTH
            ))
            if not URLMap.check_unique_short_id(short_id):
                return short_id
        raise CreatingError(CREATE_SHORT_ID_ERROR)

    @staticmethod
    def validate_short_id(short_id):
        return not (len(short_id) > MAX_SHORT_ID_SIZE or
                    not re.match(SHORT_ID_REGEXP, short_id))

    @staticmethod
    def check_unique_short_id(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def validate_url(original):
        parsed_url = urlparse(original)
        return (len(original) < MAX_ORIGINAL_SIZE and
                parsed_url.scheme and
                parsed_url.netloc)

    @staticmethod
    def create_new_url_object(
        original, custom_id, existence_message, url_message
    ):
        if not custom_id or custom_id == '':
            custom_id = URLMap.get_unique_short_id()
        if URLMap.check_unique_short_id(custom_id):
            raise ExistenceError(
                existence_message.format(custom_id=custom_id)
            )
        if (
            custom_id != '' and
            custom_id is not None and
            not URLMap.validate_short_id(custom_id)
        ):
            raise ValidationError(url_message.format(custom_id=custom_id))
        url_object = URLMap(
            original=original,
            short=custom_id
        )
        db.session.add(url_object)
        db.session.commit()
        return url_object
