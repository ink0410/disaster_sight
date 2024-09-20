from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from app.annotationTasks.models import AnnotationTask
from app.videos.schema import VideoSchema
from app import db

class AnnotationTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnnotationTask
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE  # 忽略未知字段

    annotation_task_id = fields.Integer(dump_only=True)
    video_id = fields.Integer(required=True)
    volunteer_id = fields.Integer(allow_none=True)
    annotation_task_created_time =  fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    annotation_task_begin_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    annotation_task_end_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    agency = fields.Integer(allow_none=True)