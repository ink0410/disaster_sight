from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from app.videos.models import Video
from app import db


class VideoSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Video
		sqla_session = db.session
		load_instance = True
		unknown = EXCLUDE  		#忽略未知字段

	video_id =fields.Integer(dump_only = True)
	video_stored_path = fields.String(required = True)
	video_annotated_state = fields.Integer(default=0)












