from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        description='Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        description='Ваш вариант короткой ссылки',
        validators=(Length(
            max=16,
            message="Длина не должна превышать 16 символов."), Optional(),
            Regexp(r'^[A-Za-z0-9_]+$',
                   message='недопустимое имя')
        )
    )
    submit = SubmitField('Создать')