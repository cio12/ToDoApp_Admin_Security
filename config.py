import os
from flask_bcrypt import Bcrypt
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	FLASK_ADMIN_SWATCH = 'darkly'
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-really-good-password'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SECURITY_PASSWORD_SALT = SECRET_KEY
	SECURITY_PASSWORD_HASH = 'bcrypt'

	SECURITY_REGISTERABLE = True
	SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
	
	SECURITY_POST_LOGIN_VIEW = '/admin/'
	SECURITY_POST_REGISTER_VIEW = '/admin/'
	SECURITY_POST_LOGOUT_VIEW = '/admin/'

	SECURITY_URL_PREFIX = '/admin'
	SECURITY_LOGIN_URL = '/login/'
	SECURITY_LOGOUT_URL = '/logout/'
	SECURITY_REGISTER_URL = '/register/'

	SECURITY_UNAUTHORIZED_VIEW = '/login/'
	SECURITY_SEND_REGISTER_EMAIL = False

