from flask import Flask, url_for, render_template
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, url_for_security, LoginForm, RegisterForm, user_registered
from config import Config

# create app
app = Flask(__name__)
app.config.from_object(Config)

########## ADMIN/SECURITY IMPLEMENTATION ##########

# Flaskgwt

# create database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .views import LoginView, RegisterView, UserView, ItemView, HomeView, LogoutView
from .models import UserModel, ItemModel, RoleModel
from .forms import ExtendedRegisterForm

# create security
user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# create page/pages on tool bar
admin = Admin(app, name='To Do App', index_view=HomeView(), template_mode='bootstrap3')
admin.add_view(UserView(UserModel, db.session, name='Users', endpoint='users'))
admin.add_view(ItemView(ItemModel, db.session, name='Items', endpoint='items'))
admin.add_view(LoginView(name='Login', endpoint='login'))
admin.add_view(RegisterView(name='Register', endpoint='register'))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url = url_for,
        h = admin_helpers
    )

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


