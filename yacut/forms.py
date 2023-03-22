from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length,
                                Optional, Regexp, ValidationError, URL)

from .constants import REGULAR_EXPRESSION
from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку ',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128),
                    URL(message='Проверьте корректность введёной ссылки')]
    )
    custom_id = StringField(
        'Введите Вашу короткую ссылку',
        validators=[Length(1, 16), Optional(),
                    Regexp(REGULAR_EXPRESSION, message='Только буквы и цифры')]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')
