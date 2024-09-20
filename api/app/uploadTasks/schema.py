from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from app.uploadTasks.models import UploadTask
from app.videos.schema import VideoSchema
from app import db

class UploadTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UploadTask
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE  # 忽略未知字段

    upload_task_id = fields.Integer(dump_only=True)
    upload_video_id = fields.Integer(required=True)
    upload_volunteer_id = fields.Integer(required=True)
    upload_time = fields.String(dump_only=True)
    upload_channel = fields.String(required=True)