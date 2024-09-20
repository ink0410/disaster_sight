from app import db

class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    video_stored_path = db.Column(db.String(500), nullable=False)
    video_annotated_state = db.Column(db.Integer, nullable=False)

    def __init__(self,video_stored_path, video_annotated_state=0):
        self.video_stored_path = video_stored_path
        self.video_annotated_state = video_annotated_state

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

