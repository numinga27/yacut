from http import HTTPStatus
from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import (URLMap, ID_NOT_FOUND,
                     MISSING_REQUEST,
                     SHORT_ID_GENERATION_ERROR, ShortIdGenerationError,
                     URL_REQUIRED_FIELD)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.get_url_map(short_id)
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def create():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    try:
        url_map = URLMap.create(data['url'],
                                data.get('custom_id'),
                                validate=True)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    except ShortIdGenerationError:
        raise InvalidAPIUsage(SHORT_ID_GENERATION_ERROR)

    return jsonify(url_map.url_dict()), 201
