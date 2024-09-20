from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app import db
from app.videoInformation.models import VideoInformation  # 模型类名为 VideoInformation

class VideoInformationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VideoInformation
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE  # 忽略未知字段

    video_id = fields.Integer(required=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', required=True)
    video_location = fields.Raw(allow_none=True)
    video_title = fields.String(required=True)
    disaster_type = fields.Integer(allow_none=True)
    disaster_scene = fields.Integer(allow_none=True)
    water_height = fields.Float(allow_none=True)
    water_speed = fields.Float(allow_none=True)
    potential_landmark = fields.Raw(allow_none=True)
    video_help_information = fields.String(allow_none=True)
    video_description = fields.String(allow_none=True)