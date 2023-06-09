import os
import re
from string import ascii_letters, digits


ALLOWED_SYMBOLS = ascii_letters + digits
GENERATION_NUMBER = 10
MAX_CUSTOM_ID_SIZE = 16
MAX_ORIGINAL_SIZE = 2048
CUSTOM_ID_LENGTH = 6
CUSTOM_ID_REGEXP = re.compile(rf'^[{re.escape(ALLOWED_SYMBOLS)}]+$')
REDIRECT_FUNCTION = 'redirect_to_original'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='supersecretkey')
