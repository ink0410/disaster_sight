from app import db
from app.videos.models import Video
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry


class MapView(db.Model):
    __tablename__ = 'mapView'
    map_video_id = Column(Integer,ForeignKey('videos.video_id'), primary_key=True, unique=True,)
    location = Column(Geometry('POINT'), nullable=True)


    def __init__(self, location=None, map_video_id=None):
        self.location = location
        self.map_video_id = map_video_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self