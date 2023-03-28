import os
import re
import string


CREATE_SET = string.ascii_letters + string.digits
CUSTOM_ID_LEN = 6
PATTERN = f'[{re.escape(CREATE_SET)}]'
LEN = 16
ORIGINAL_LEN = 2048
ITERATIONS_COUNT = 100


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')