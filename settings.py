import os
import re
import string


CHARACTERS_SET = string.ascii_letters + string.digits
PATTERN = f'[{re.escape(CHARACTERS_SET)}]'
LEN = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')