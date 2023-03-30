from http import HTTPStatus
from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap, ID_NOT_FOUND, MISSING_REQUEST, URL_REQUIRED_FIELD


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.get_url_map(short_id)
    if not url:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})


@app.route('/api/id/', methods=['POST'])
def create():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    try:
        url = URLMap.create(data['url'], data.get('custom_id'), validate=True)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url.url_dict()), 201
