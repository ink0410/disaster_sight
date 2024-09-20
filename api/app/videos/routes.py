from flask import request,jsonify,make_response
from app import db
from app.videos import videos_bp
from app.videos.models import Video
from app.videos.schema import VideoSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from sqlalchemy.exc import IntegrityError
#select all操作
@videos_bp.route('/', methods=['GET'])
def get_videos():
	videos = Video.query.all()
	result = [
		{
			'video_id': video.video_id,
			'video_stored_path': video.video_stored_path,
			'video_annotated_state': video.video_annotated_state
		} for video in videos
	]
	return jsonify(result)


# select_by_id操作
@videos_bp.route('/<int:video_id>', methods=['GET'])
def get_video_by_id(video_id):
    get_video = Video.query.get(video_id)
    video_schema = VideoSchema()
    video = video_schema.dump(get_video)
    return make_response(jsonify({"video": video}))


# insert操作
@videos_bp.route('/', methods=['POST'])
def create_video():
    try:
        data = request.get_json()
        video_schema = VideoSchema()
        video = video_schema.load(data, session=db.session)
        db.session.add(video)  # 直接使用 SQLAlchemy 的会话方法保存到数据库
        db.session.commit()
        result = video_schema.dump(video)
        print(result)
        return make_response(jsonify({"video": result}), 201)
        
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Integrity error occurred"}), 422)
    except Exception as e:
        print(f"insert失败的原因是：{e}")
        db.session.rollback()
        return make_response(jsonify({"message": "Invalid input"}), 422)


# update操作
@videos_bp.route('/<video_id>', methods=['PUT'])
def update_video_by_id(video_id):
    data = request.get_json()
    get_video = Video.query.get(video_id)
    if not get_video:
        return jsonify({"error": "Video not found"}), 40
    if data.get('video_stored_path'):
        get_video.ideo_stored_path = data['video_stored_path']
    if data.get('video_annotated_state'):
        get_video.video_annotated_state = data['video_annotated_state']


    db.session.add(get_video)
    db.session.commit()
    video_schema = VideoSchema(only=['video_id', 'video_stored_path', 'video_annotated_state'])
    video = video_schema.dump(get_video)
    return jsonify({"message": "Video updated successfully"}), 200


# delete操作
@videos_bp.route('/<video_id>', methods=['DELETE'])
def delete_video_by_id(video_id):
    get_video = Video.query.get(video_id)
    db.session.delete(get_video)
    db.session.commit()
    return make_response({"msg": "ok"}, 204)