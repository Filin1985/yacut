from http import HTTPStatus

from flask import jsonify, request

from .error_handlers import InvalidAPIUsage, ExistenceError, ValidationError
from .models import URLMap
from . import app


EMPTY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
SHORT_ID_EXISTS = 'Имя "{custom_id}" уже занято.'
UNACCEPTABLE_URL = 'Указано недопустимое имя для короткой ссылки'


@app.route('/api/id/', methods=['POST'])
def post_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED)
    original = data.get('url')
    custom_id = data.get('custom_id', None)
    try:
        url_object = URLMap.create_urlmap(
            original, custom_id, SHORT_ID_EXISTS
        )
    except ExistenceError as error:
        return jsonify(error.to_dict()), error.status_code
    except ValidationError as error:
        return jsonify(error.to_dict()), error.status_code
    return jsonify(url_object.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_object = URLMap.get_unique_custom_id(short_id)
    if url_object is not None:
        return jsonify({'url': url_object.original})
    raise InvalidAPIUsage(
        'Указанный id не найден',
        HTTPStatus.NOT_FOUND
    )
