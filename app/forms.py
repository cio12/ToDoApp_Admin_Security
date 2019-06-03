from flask_security.forms import RegisterForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from .models import UserModel

class ExtendedRegisterForm(RegisterForm):
	name = StringField('Name', validators=[DataRequired()])
	password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')




