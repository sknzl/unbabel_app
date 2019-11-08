from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TextForm(FlaskForm):
    translation_text = TextAreaField('Enter english text', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 5})
    submit = SubmitField('Translate to spanish')