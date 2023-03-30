import os
import re
import string


CHARACTERS_SET = string.ascii_letters + string.digits
PATTERN = f'[{re.escape(CHARACTERS_SET)}]'
CUSTOM_ID_LEN = 6
SHORT_LEN = 16
ORIGINAL_LEN = 2048
ITERATIONS_COUNT = 100
REGULAR_EXPRESSION = '^[a-zA-Z0-9]*$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
