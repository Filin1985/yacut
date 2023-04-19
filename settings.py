import os


MAX_SYMBOLS = 6
GENERATION_NUMBER = 10
MAX_SHORT_ID_SIZE = 16
MAX_ORIGINAL_SIZE = 2048
SHORT_LENGTH = 6


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='supersecretkey')
