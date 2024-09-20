from app import db
from datetime import datetime
import json
from app.videos.models import Video

class VideoInformation(db.Model):
    __tablename__ = 'videoInformation'

    video_id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False)
    video_location = db.Column(db.JSON, nullable=True)
    video_title = db.Column(db.String(255), nullable=False)
    disaster_type = db.Column(db.Integer, nullable=True)
    disaster_scene = db.Column(db.Integer, nullable=True)
    water_height = db.Column(db.Float, nullable=True)
    water_speed = db.Column(db.Float, nullable=True)
    potential_landmark = db.Column(db.JSON, nullable=True)
    video_help_information = db.Column(db.String(255), nullable=True)
    video_description = db.Column(db.String(450), nullable=True)

    def __init__(self,video_id, video_location=None,create_time=None, video_title=None, disaster_type=None, disaster_scene=None,
                 water_height=None, water_speed=None, potential_landmark=None,
                 video_help_information=None, video_description=None):
        self.video_id = video_id
        self.create_time = create_time
        self.video_location = video_location
        self.video_title = video_title
        self.disaster_type = disaster_type
        self.disaster_scene = disaster_scene
        self.water_height = water_height
        self.water_speed = water_speed
        self.potential_landmark = potential_landmark
        self.video_help_information = video_help_information
        self.video_description = video_description

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'video_id': self.video_id,
            'create_time': self.create_time,
            'video_location': json.loads(self.video_location) if self.video_location else None,
            'video_title': self.video_title,
            'disaster_type': self.disaster_type,
            'disaster_scene': self.disaster_scene,
            'water_height': self.water_height,
            'water_speed': self.water_speed,
            'potential_landmark': json.loads(self.potential_landmark) if self.potential_landmark else None,
            'video_help_information': self.video_help_information,
            'video_description': self.video_description
        }

