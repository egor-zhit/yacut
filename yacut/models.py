from datetime import datetime
from random import choices
import re
from string import ascii_letters, digits

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(64), unique=True,)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short_id():
        short = ''.join(choices(ascii_letters + digits, k=6))
        if not URLMap.query.filter_by(short=short).first():
            return short

    def checking_characters(text):
        if not len(text) <= 16:
            return False
        return bool(re.match('^[a-zA-Z0-9]+$', text))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_url', short_url=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        columns_dict = {'original': 'url', 'short': 'custom_id'}
        for field in columns_dict:
            if field[1] in data:
                setattr(self, field[0], data[field[1]])