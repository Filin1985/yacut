from http import HTTPStatus

from flask import jsonify, request

from .constants import (
    EMPTY_REQUEST,
    SHORT_ID_EXISTS,
    INCORRECT_URL,
    URL_REQUIRED,
    UNACCEPTABLE_URL
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_validity_shirt_id, check_original_url
from . import app, db


@app.route('/api/id/', methods=['POST'])
def post_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED)
    original = data.get('url')
    url_object = URLMap()
    custom_id = data.get('custom_id', None)
    if not check_original_url(original):
        raise InvalidAPIUsage(INCORRECT_URL)
    if not custom_id or custom_id == '':
        custom_id = url_object.get_unique_short_id()
        data.update({'custom_id': custom_id})
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            SHORT_ID_EXISTS.format(custom_id=custom_id)
        )
    if not check_validity_shirt_id(custom_id):
        raise InvalidAPIUsage(
            UNACCEPTABLE_URL,
            HTTPStatus.BAD_REQUEST
        )
    url_object.from_dict(data)
    db.session.add(url_object)
    db.session.commit()
    return jsonify(url_object.to_dict()), HTTPStatus.CREATED

@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_object = URLMap.query.filter_by(short=short_id).first()
    if url_object is not None:
        return jsonify({'url': url_object.original})
    raise InvalidAPIUsage(
        'Указанный id не найден',
        HTTPStatus.NOT_FOUND
    )
