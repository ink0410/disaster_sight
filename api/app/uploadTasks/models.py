from app import db
from app.videos.models import Video
from datetime import datetime

class UploadTask(db.Model):
	__tablename__ = 'uploadTasks'
	upload_task_id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
	upload_video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=False)
	upload_volunteer_id = db.Column(db.Integer, nullable=False)
	upload_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	upload_channel = db.Column(db.String(256), nullable=False)
	
	def __init__(self,upload_video_id, upload_volunteer_id, upload_channel):
		self.upload_video_id = upload_video_id
		self.upload_volunteer_id = upload_volunteer_id
		self.upload_channel = upload_channel

	def create(self):
		db.session.add(self)
		db.session.commit()
		return self