from http import HTTPStatus

from flask import jsonify, request

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from . import app


EMPTY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
INCORRECT_URL = 'Введите корректный URL адрес'
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
    if not URLMap.validate_url(original):
        raise InvalidAPIUsage(INCORRECT_URL)
    custom_id = data.get('custom_id', None)
    try:
        url_object = URLMap.create_new_url_object(
            original, custom_id, SHORT_ID_EXISTS, UNACCEPTABLE_URL
        )
    except Exception as error:
        return jsonify(error.to_dict()), error.status_code
    return jsonify(url_object.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_object = URLMap.check_unique_short_id(short_id)
    if url_object is not None:
        return jsonify({'url': url_object.original})
    raise InvalidAPIUsage(
        'Указанный id не найден',
        HTTPStatus.NOT_FOUND
    )
