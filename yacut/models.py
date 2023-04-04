import random

import validators
from datetime import datetime
from flask import url_for
from re import fullmatch

from settings import (GENERATE_STRING_SHORT_ID, CUSTOM_ID_LEN_LIMIT,
                      ITERATIONS_COUNT_SHORT_ID,
                      ORIGINAL_LEN, SHORT_ID_LEN_LIMIT,
                      REGULAR_EXPRESSION_SHORT_ID)

from . import db
from .error_handlers import InvalidAPIUsage


ID_NOT_FOUND = 'Указанный id не найден'
MISSING_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
ERROR_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
NAME_NOT_FREE = 'Имя "{}" уже занято.'
SHORT_ID_GENERATION_ERROR = 'Короткая ссылка не может быть создана'
URL_ERROR = 'Указан недопустимый URL'
ERROR_LEN_ORIGINAL = ('Ошибка. Длина исходной ссылки не может превышать {}'
                      'Текущая длина ссылки{}')
TEST_LEN_SHORT_ID = (REGULAR_EXPRESSION_SHORT_ID +
                     f'{{1,{SHORT_ID_LEN_LIMIT}}}')


class ShortIdGenerationError(Exception):
    pass


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(SHORT_ID_LEN_LIMIT), nullable=False)
    original = db.Column(db.String(ORIGINAL_LEN), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def url_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short_id=self.short, _external=True
            )
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def get_url_map_or_404(short_id):
        return URLMap.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def get_unique_short_id():
        for _ in range(ITERATIONS_COUNT_SHORT_ID):
            short_id = ''.join(random.sample(
                GENERATE_STRING_SHORT_ID,
                CUSTOM_ID_LEN_LIMIT
            ))
            if not URLMap.get_url_map(short_id):
                return short_id
        raise ShortIdGenerationError(SHORT_ID_GENERATION_ERROR)

    @staticmethod
    def get_url_map(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def create(original, short_id=None, validate=False):
        if validate or not validate:
            if short_id in [None, ""]:
                short_id = URLMap.get_unique_short_id()
            original_len_now = len(original)
            if original_len_now > ORIGINAL_LEN:
                raise ValueError(
                    ERROR_LEN_ORIGINAL.format(
                        ORIGINAL_LEN,
                        original_len_now
                    )
                )
            if not validators.url(original):
                raise ValueError(URL_ERROR)
            if not fullmatch(
                    TEST_LEN_SHORT_ID,
                    short_id):
                raise ValueError(ERROR_SHORT_LINK)
            if len(short_id) > SHORT_ID_LEN_LIMIT:
                raise InvalidAPIUsage(ERROR_SHORT_LINK)
            if URLMap.get_url_map(short_id):
                raise ValueError(NAME_NOT_FREE.format(short_id))
        url_map = URLMap(original=original, short=short_id)
        db.session.add(url_map)
        db.session.commit()

        return url_map
