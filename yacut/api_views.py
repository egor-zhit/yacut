from http import HTTPStatus
from flask import request
from flask import jsonify

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = URLMap.get_unique_short_id()
    if not URLMap.checking_characters(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    url_map = URLMap(original=data.get('url'), short=data['custom_id'])
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED.value


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND.value)
    return jsonify({'url': urlmap.to_dict()['url']}), HTTPStatus.OK.value