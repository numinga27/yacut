from http import HTTPStatus
from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap, ID_NOT_FOUND


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_url(short_url):
    url = URLMap().get_url_map(short_url)
    if not url:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    try:
        url = URLMap.add_u(data)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url.url_dict()), HTTPStatus.CREATED
