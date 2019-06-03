from app import db
from flask_security import UserMixin, RoleMixin
from flask_bcrypt import generate_password_hash, check_password_hash

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

class RoleModel(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

    def __repr__(self):
    	return '{}'.format(self.name)
    	
class UserModel(db.Model, UserMixin):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(128))
	active = db.Column(db.Boolean())
	items = db.relationship('ItemModel', backref='author', lazy='dynamic')
	roles = db.relationship('RoleModel', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

	def set_password(self, password):
		self.password = generate_password_hash(password).decode('UTF-8')

	def check_password(self, password):
		return check_password_hash(self.password, password)
				
	def __repr__(self):
		return '{}'.format(self.name)

class ItemModel(db.Model):
	__tablename__ = 'item'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	time = db.Column(db.String(10), index=True)
	deadline = db.Column(db.String(10))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '{}'.format(self.body)



