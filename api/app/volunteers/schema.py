from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from app.volunteers.models import Volunteer
from app import db

class VolunteerSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Volunteer
		sqla_session = db.session
		load_instance = True
		unknown = EXCLUDE  		#忽略未知字段

	volunteer_id =fields.Integer(required=True)
	volunteer_name = fields.String(required = True)
	volunteer_phone_number = fields.String(required = True)
	volunteer_level = fields.Integer()
	volunteer_login_pwd = fields.String(required = True)
