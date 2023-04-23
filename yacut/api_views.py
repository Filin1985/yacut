from http import HTTPStatus

from flask import jsonify, request

from .error_handlers import InvalidAPIUsage, ExistenceError, ValidationError
from .models import URLMap
from . import app


EMPTY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
SHORT_ID_EXISTS = 'Имя "{custom_id}" уже занято.'


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
        urlmap_object = URLMap.create_urlmap(
            original, custom_id
        )
    except ExistenceError:
        raise InvalidAPIUsage(SHORT_ID_EXISTS.format(custom_id=custom_id))
    except ValidationError as error:
        raise InvalidAPIUsage(error.message)
    return jsonify(urlmap_object.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    urlmap_object = URLMap.get_urlmap_item(short_id)
    if urlmap_object is not None:
        return jsonify({'url': urlmap_object.original})
    raise InvalidAPIUsage(
        'Указанный id не найден',
        HTTPStatus.NOT_FOUND
    )
