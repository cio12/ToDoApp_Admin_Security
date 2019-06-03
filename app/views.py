from flask_admin.contrib.sqla.view import ModelView, func
from flask_admin import AdminIndexView, BaseView, expose
from flask_security import LoginForm, login_required, roles_required, logout_user, login_user, utils, current_user, auth_token_required
from .forms import ExtendedRegisterForm
from .models import UserModel
from app import db

class HomeView(AdminIndexView):
	@expose('/')
	#@auth_token_required
	def index(self):
		return self.render('admin/index.html')

class UserView(ModelView):

	column_list = ['name','email', 'password', 'roles', 'active']
	column_exclude_list = ['password', 'roles']
	column_sortable_list = ['name','email']
	column_searchable_list = ['name', 'email']

	create_modal = True
	form_create_rules = ('name','email', 'password', 'roles')

	edit_modal = True
	form_edit_rules = ('name','email', 'password', 'roles')
	
	def is_accessible(self):
		if current_user.has_role('admin'):
			return True
		else:
			return False
	
	
class ItemView(ModelView):

	column_list = ['author', 'body', 'time', 'deadline']
	column_sortable_list = ['time', 'deadline']
	column_searchable_list = ['time', 'deadline']

	create_modal = True
	form_create_rules = ('author', 'body', 'time', 'deadline')

	edit_modal = True
	form_edit_rules = ('author', 'body', 'time', 'deadline')
	
	def get_query(self):
		if not current_user.is_authenticated:
			return self.session.query(self.model).filter(self.model.author==None)
		elif current_user.has_role('admin'):
			return self.session.query(self.model)
		else:
			return self.session.query(self.model).filter(self.model.author==current_user)


	def get_count_query(self):
		if not current_user.is_authenticated:
			return self.session.query(func.count('*')).filter(self.model.author==None)
		elif current_user.has_role('admin'):
			return self.session.query(func.count('*'))
		else:
			return self.session.query(func.count('*')).filter(self.model.author==current_user)

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False
		return True

class LoginView(BaseView):
	@expose('/')
	def index(self):
		form = LoginForm()
		return self.render('security/login_user.html', login_user_form=form)

	def is_accessible(self):
		if current_user.is_active or current_user.is_authenticated:
			return False
		return True

class LogoutView(BaseView):
	@expose('/')
	@login_required
	def index(self):
		logout_user()
		return redirect(url_for('admin.index'))

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False
		return True

class RegisterView(BaseView):
	@expose('/')
	def index(self):
		form = ExtendedRegisterForm()
		register()
		return self.render('security/register_user.html', register_user_form=form)

	def is_accessible(self):
		if current_user.is_active or current_user.is_authenticated:
			return False
		return True




