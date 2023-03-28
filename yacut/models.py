import re
import random
import string

from datetime import datetime
from flask import url_for

from . import db
from .constants import REGULAR_EXPRESSION
from settings import PATTERN, LEN
from .error_handlers import InvalidAPIUsage

ID_NOT_FOUND = 'Указанный id не найден'
MISSING_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
URL_ERROR = 'Указан недопустимый URL'
ERROR_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
NAME_NOT_FREE = 'Имя "{}" уже занято.'
SHORT_ID_GENERATION_ERROR = 'Короткая ссылка не может быть создана'
ERROR_LEN_ORIGINAL = ('Ошибка. Длина исходной ссылки не может превышать {}'
                      'Текущая длина ссылки{}')
PATTERN_SHORT_ID = PATTERN + f'{{1,{LEN}}}'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(16), nullable=False)
    original = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def url_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short_url=self.short, _external=True
            )
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def get_url_map_or_404(short_url):
        return URLMap.query.filter_by(short=short_url).first_or_404()

    @staticmethod
    def get_unique_short_id():
        letters_digits = string.ascii_letters + string.digits
        for _ in range(100):
            short_url = ''.join(random.sample(letters_digits, 6))
            if not URLMap.get_url_map(short_url):
                return short_url

    @staticmethod
    def get_url_map(short_url):
        return URLMap.query.filter_by(short=short_url).first()

    @staticmethod
    def add_u(data):
        if not data:
            raise InvalidAPIUsage('Отсутствует тело запроса')
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        if ('custom_id' not in data or
            data['custom_id'] == '' or
                data['custom_id'] is None):
            data['custom_id'] = URLMap.get_unique_short_id()
        if URLMap.get_url_map(data['custom_id']) is not None:
            custom_id = data['custom_id']
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        if (re.match(REGULAR_EXPRESSION, data['custom_id']) is None or
                len(data['custom_id']) > 16):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        url = URLMap()
        url.from_dict(data)
        db.session.add(url)
        db.session.commit()

        return url
