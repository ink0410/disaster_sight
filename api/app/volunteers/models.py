from app import db
from passlib.hash import pbkdf2_sha256 as sha256
#from marshmallow import fields
from sqlalchemy import Computed

class Volunteer(db.Model):
	__tablename__ = 'volunteers'
	volunteer_id = db.Column(db.Integer)
	volunteer_name = db.Column(db.String(80), nullable=False)
	volunteer_phone_number = db.Column(db.String(80), nullable=False, primary_key=True)
	volunteer_login_pwd = db.Column(db.String(256), nullable=False)
	volunteer_level = db.Column(db.Integer, Computed('((((((floor((volunteer_id / 100000)) + (floor((volunteer_id / 10000)) % 10)) + (floor((volunteer_id / 1000)) % 10)) + (floor((volunteer_id / 100)) % 10)) + (floor((volunteer_id / 10)) % 10)) + (volunteer_id % 10)) % 3)'), nullable=False)
	
	def __init__(self, volunteer_id, volunteer_name, volunteer_phone_number, volunteer_login_pwd):
		self.volunteer_id = volunteer_id
		self.volunteer_name = volunteer_name
		self.volunteer_phone_number = volunteer_phone_number
		self.volunteer_login_pwd = volunteer_login_pwd

	def create(self):
		db.session.add(self)
		db.session.commit()
		return self
	
	@classmethod
	def find_by_phoneNumber(cls,volunteer_phone_number):
		return cls.query.filter_by(volunteer_phone_number=volunteer_phone_number).first()

	@staticmethod
	def generate_hash(volunteer_login_pwd):
		return sha256.hash(volunteer_login_pwd)

	@staticmethod
	def verify_hash(volunteer_login_pwd,hash):
		return sha256.verify(volunteer_login_pwd,hash)
	