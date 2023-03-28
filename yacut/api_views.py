# import re
from http import HTTPStatus
from flask import jsonify, request

from . import app
# from .constants import REGULAR_EXPRESSION
from .error_handlers import InvalidAPIUsage
from .models import URLMap
# from .views import get_unique_short_id


# @app.route('/api/id/<string:short_url>/', methods=['GET'])
# def get_url(short_url):
# url = URLMap.query.filter_by(short=short_url).first()
# if url is None:
#     raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
# data = url.url_dict()
# return jsonify({'url': data['url']}), HTTPStatus.OK

@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_url(short_url):
    url = URLMap().get_url_map(short_url)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    # return url.valid_id(short_url)
    return jsonify({'url': url.original})


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    try:
        url = URLMap.add_u(data)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url.url_dict()), HTTPStatus.CREATED
