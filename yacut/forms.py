from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length,
                                Optional, Regexp, ValidationError, URL)

from .constants import REGULAR_EXPRESSION
from .models import URLMap


INSERT = 'Введите ссылку '
REQUERED_FIELD = 'Обязательное поле'
CORRECT_INSERT = 'Проверьте корректность введёной ссылки'
OWN_LINK = 'Введите Вашу короткую ссылку'
LIMIT = 'Только буквы и цифры'
CREAT = 'Создать'
VALID_FIELD = 'Имя {} уже занято!'


class URLForm(FlaskForm):
    original_link = URLField(
        INSERT,
        validators=[DataRequired(message=REQUERED_FIELD),
                    Length(1, 128),
                    URL(require_tld=True, message=CORRECT_INSERT)]
    )
    custom_id = StringField(
        OWN_LINK,
        validators=[Length(1, 16), Optional(),
                    Regexp(REGULAR_EXPRESSION, message=LIMIT)]
    )
    submit = SubmitField(CREAT)

    def validate_custom_id(self, field):
        if field.data and URLMap.get_url_map(field.data):
            raise ValidationError(VALID_FIELD.format(field.data))
        return field.data
