from flask import request,jsonify,make_response
from app import db
from app.uploadTasks import uploadTasks_bp
from app.uploadTasks.models import UploadTask
from app.uploadTasks.schema import UploadTaskSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from datetime import datetime

#select all操作
@uploadTasks_bp.route('/', methods=['GET'])
def get_uploadTasks_list():
    fetched = UploadTask.query.all()
    uploadTask_schema = UploadTaskSchema(many=True,only=['upload_task_id','upload_video_id','upload_volunteer_id','upload_time','upload_channel'])
    uploadTasks = uploadTask_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"uploadTasks":uploadTasks})



# select_by_id操作
@uploadTasks_bp.route('/<int:upload_task_id>',methods=['GET'])
def get_upload_task_by_id(upload_task_id):
    fetched = UploadTask.query.get_or_404(upload_task_id)
    uploadTask_schema = UploadTaskSchema()
    uploadTask = uploadTask_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"uploadTask":uploadTask})


# insert操作
@uploadTasks_bp.route('/upload', methods=['POST'])
def create_uploadTask():
    try:
        data = request.get_json()
        print(data)
        uploadTask_schema = UploadTaskSchema()
        uploadTask = uploadTask_schema.load(data,session=db.session)
        uploadTask.upload_time = datetime.utcnow()  # 设置默认值
        db.session.add(uploadTask)
        db.session.commit()
        result = uploadTask_schema.dump(uploadTask)
        return response_with(resp.SUCCESS_201,value={"uploadTask":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

# update操作
@uploadTasks_bp.route('/<int:upload_task_id>',methods=['PUT'])
def update_uploadTask_detail(upload_task_id):
    data = request.get_json()
    get_upload_task = UploadTask.query.get_or_404(upload_task_id)
    if data.get('upload_volunteer_id'):
        get_upload_task.upload_volunteer_id = data['upload_volunteer_id']

    if data.get('upload_channel'):
        get_upload_task.upload_channel = data['upload_channel']

    if data.get('upload_video_id'):
        get_upload_task.upload_video_id = data['upload_video_id']

    db.session.add(get_upload_task)
    db.session.commit()
    upload_task_schema = UploadTaskSchema()
    upload_task = upload_task_schema.dump(get_upload_task)
    return response_with(resp.SUCCESS_200,value={"upload_task":upload_task})


# delete操作
@uploadTasks_bp.route('/<upload_task_id>', methods=['DELETE'])
def delete_upload_task_by_id(upload_task_id):
    get_upload_task = UploadTask.query.get(upload_task_id)
    db.session.delete(get_upload_task)
    db.session.commit()
    return make_response({"msg": "ok"}, 204)