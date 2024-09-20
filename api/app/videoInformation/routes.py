import json
from flask import  request, jsonify, make_response
from app import db
from app.videoInformation import videoInformation_bp
from app.videoInformation.models import VideoInformation  # 模型类名为 VideoInformation
from app.videoInformation.schema import VideoInformationSchema  # 序列化类名为 VideoInformationSchema
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
from app.utils import responses as resp
from app.utils.responses import response_with

# Select all 操作
@videoInformation_bp.route('/', methods=['GET'])
def get_videoInformation():
    videoInformation = VideoInformation.query.all()
    videoInformation_schema = VideoInformationSchema(many=True)
    result = videoInformation_schema.dump(videoInformation)
    return jsonify(result)


# Select by ID 操作
@videoInformation_bp.route('/<int:video_id>', methods=['GET'])
def get_videoInformation_by_id(video_id):
    videoInformation = VideoInformation.query.get_or_404(video_id)
    videoInformation_schema = VideoInformationSchema()
    return make_response(jsonify({"videoInformation": videoInformation_schema.dump(videoInformation)}))


# Insert 操作
@videoInformation_bp.route('/upload', methods=['POST'])
def create_videoInformation():
    try:
        data = request.get_json()
        print(data)
        try:
            dt = datetime.strptime(data['create_time'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=None)
            data['create_time'] = dt
            print("转换后的 create_time:", data['create_time'])
            print("更新后的 data:", data)
        except ValueError as e:
            return jsonify({"message": "Invalid datetime format"}), 422 
        print(data)
        videoInformation_schema = VideoInformationSchema()
     #(f"Data before loading into schema: {data}")  # 打印加载到 schema 之前的数据
        videoInformation = videoInformation_schema.load(data, session=db.session)
     #print(f"Data after loading into schema: {videoInformation}")  # 打印加载到 schema 之后的数据
        db.session.add(videoInformation)
        db.session.commit()
        return response_with(resp.SUCCESS_200,value={"videoInformation": videoInformation_schema.dump(videoInformation)})

    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Integrity error occurred"}), 422)
    except Exception as e:
        db.session.rollback()
        print(e)
        return make_response(jsonify({"message": "Invalid input"}), 422)

# Update 操作
@videoInformation_bp.route('/<int:video_id>', methods=['PUT'])
def update_videoInformation_by_id(video_id):
    try:
        data = request.get_json()
        videoInformation = VideoInformation.query.get_or_404(video_id)
        videoInformation_schema = VideoInformationSchema()

        if not videoInformation:
            return jsonify({"error": "VideoInformation not found"}), 404

        if 'create_time' in data:
            try:
                data['create_time'] = datetime.strptime(data['create_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                return jsonify({"message": "Invalid datetime format"}), 422

        if data.get('disaster_type'):
            videoInformation.disaster_type = data['disaster_type']
        if data.get('disaster_scene'):
            videoInformation.disaster_scene = data['disaster_scene']
        if data.get('water_height'):
            videoInformation.water_height = data['water_height']
        if data.get('water_speed'):
            videoInformation.water_speed = data['water_speed']
        if data.get('potential_landmark'):
            videoInformation.potential_landmark = data['potential_landmark']
        if data.get('video_description'):
            videoInformation.video_description = data['video_description']
        if data.get('video_help_information'):
            videoInformation.video_help_information = data['video_help_information']

        # 更新 create_time 字段
        if 'create_time' in data:
            videoInformation.create_time = data['create_time']
        else:
            # 确保 create_time 字段保持为 datetime 对象
            videoInformation.create_time = videoInformation.create_time if isinstance(videoInformation.create_time, datetime) else datetime.strptime(videoInformation.create_time, '%Y-%m-%d %H:%M:%S')

        db.session.commit()
        return make_response(jsonify({"videoInformation": videoInformation_schema.dump(videoInformation)}), 200)
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")  # 打印数据库完整性错误信息
        return jsonify({"message": "Integrity error occurred"}), 422
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")  # 打印其他异常信息
        return jsonify({"message": "Invalid input"}), 422
    
# Delete 操作
@videoInformation_bp.route('/<int:video_id>', methods=['DELETE'])
def delete_videoInformation_by_id(video_id):
    videoInformation = VideoInformation.query.get_or_404(video_id)
    db.session.delete(videoInformation)
    db.session.commit()
    return make_response({"msg": "VideoInformation deleted successfully"}, 204)