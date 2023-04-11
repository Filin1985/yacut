from http import HTTPStatus
from flask import jsonify, request

from . import app, db
from .constants import EMPTY_REQUEST, SHORT_ID_EXISTS
from .error_handlers import InvalidAPIUsage
from .models import URLMap

@app.route('/api/id/', methods=['POST'])
def post_short_url():
    data = request.get_json()
    custom_id = data.get('custom_id', None)
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    url_object = URLMap()
    if custom_id is None:
        custom_id = url_object.generate_short_id()
        data.update({'custom_id': custom_id})
    if URLMap.query.filter_by(short=custom_id).first() is not None:
         raise InvalidAPIUsage(SHORT_ID_EXISTS)
    url_object.from_dict(data)
    db.session.add(url_object)
    db.session.commit()
    return jsonify(url_object.to_dict()), HTTPStatus.CREATED

@app.route('/api/id/<string:short_id>', methods=['GET'])
def get_short_url(short_id):
    url_object = URLMap.query.filter_by(short=short_id).first()
    if url_object is not None:
        return jsonify({'opinion': url_object.to_dict()}),  HTTPStatus.OK
    raise InvalidAPIUsage('В базе данных нет мнений', HTTPStatus.NOT_FOUND)
    