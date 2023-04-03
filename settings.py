import os
import re
import string


GENERATE_STRING = string.ascii_letters + string.digits
REGULAR_EXPRESSION = f'[{re.escape(GENERATE_STRING)}]'
CUSTOM_ID_LEN_LIMIT = 6
SHORT_ID_LEN_LIMIT = 16
ORIGINAL_LEN = 2048
ITERATIONS_COUNT = 100


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
