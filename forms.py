from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    prompt = StringField("Enter Your Query:", validators=[DataRequired()])
    submit = SubmitField("Search")
