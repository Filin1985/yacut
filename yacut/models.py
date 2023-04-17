from datetime import datetime
import random
from string import ascii_letters, digits

from flask import url_for

from .constants import MAX_SYMBOLS
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_to_original', short_url=self.short, _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def get_unique_short_id(self):
        short_link = ''.join(
            random.choices(ascii_letters + digits, k=MAX_SYMBOLS)
        )
        if not self.query.filter_by(short=short_link).first():
            return short_link
        return self.get_unique_short_id()
