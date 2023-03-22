from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(16), nullable=False)
    original = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def url_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short_url=self.short, _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
