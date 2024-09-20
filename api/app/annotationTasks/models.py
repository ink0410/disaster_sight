from app import db
from datetime import datetime

class AnnotationTask(db.Model):
	__tablename__ = 'annotationTasks'
	annotation_task_id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
	video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=False)
	volunteer_id = db.Column(db.Integer, nullable=False,default=-1)
	annotation_task_begin_time= db.Column(db.DateTime, nullable=False, default=datetime(1000,1,1,0,0,0))
	annotation_task_end_time= db.Column(db.DateTime, nullable=False, default=datetime(1000,1,1,0,0,0))
	agency= db.Column(db.Integer, nullable=False)
	annotation_task_created_time= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
	def __init__(self,video_id, annotation_task_created_time=None, volunteer_id=-1,annotation_task_begin_time=datetime(1000,1,1,0,0,0),annotation_task_end_time=datetime(1000,1,1,0,0,0),agency=None):
		self.video_id = video_id
		self.annotation_task_created_time = annotation_task_created_time or datetime.utcnow
		self.volunteer_id=volunteer_id
		self.annotation_task_begin_time = annotation_task_begin_time
		self.annotation_task_end_time = annotation_task_end_time
		self.agency = agency
		
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self