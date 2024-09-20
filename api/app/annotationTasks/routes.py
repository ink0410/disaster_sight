from flask import request,jsonify,make_response
from app import db
from app.annotationTasks import annotationTasks_bp
from app.annotationTasks.models import AnnotationTask
from app.annotationTasks.schema import AnnotationTaskSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from datetime import datetime

#select all操作
@annotationTasks_bp.route('/', methods=['GET'])
def get_annotationTasks_list():
    fetched = AnnotationTask.query.all()
    annotationTask_schema = AnnotationTaskSchema(many=True,only=['annotation_task_id','video_id','volunteer_id','annotation_task_created_time','annotation_task_begin_time','annotation_task_end_time','agency'])
    annotationTasks = annotationTask_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"annotationTasks":annotationTasks})

# select_by_id操作
@annotationTasks_bp.route('/<int:annotation_task_id>',methods=['GET'])
def get_annotation_task_by_id(annotation_task_id):
    fetched = AnnotationTask.query.get_or_404(annotation_task_id)
    annotationTask_schema = AnnotationTaskSchema()
    annotationTask = annotationTask_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"annotationTask":annotationTask})

#insert操作
@annotationTasks_bp.route('/', methods=['POST'])
def create_annotationTask():
    try:
        data = request.get_json()
        print(data)
        annotationTask_schema = AnnotationTaskSchema()
        annotationTask = annotationTask_schema.load(data,session=db.session)
        annotationTask.annotation_task_created_time = datetime.utcnow()  # 设置默认值
        db.session.add(annotationTask)
        db.session.commit()
        result = annotationTask_schema.dump(annotationTask)
        return response_with(resp.SUCCESS_201,value={"annotationTask":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

# update操作
@annotationTasks_bp.route('/<int:annotation_task_id>',methods=['PUT'])
def update_annotationTask_detail(annotation_task_id):
    data = request.get_json()
    get_annotation_task = AnnotationTask.query.get_or_404(annotation_task_id)
    if data.get('volunteer_id'):
        get_annotation_task.volunteer_id = data['volunteer_id']

    if data.get('agency'):
        get_annotation_task.agency = data['agency']

    if 'annotation_task_begin_time' in data:
            try:
                data['annotation_task_begin_time'] = datetime.strptime(data['annotation_task_begin_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                return jsonify({"message": "Invalid datetime format"}), 422
    if 'annotation_task_end_time' in data:
            try:
                data['annotation_task_end_time'] = datetime.strptime(data['annotation_task_end_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                return jsonify({"message": "Invalid datetime format"}), 422


    db.session.add(get_annotation_task)
    if 'annotation_task_begin_time' in data:
            get_annotation_task.create_time = data['annotation_task_begin_time']
    else:
            # 确保 create_time 字段保持为 datetime 对象
            get_annotation_task.annotation_task_begin_time = get_annotation_task.annotation_task_begin_time if isinstance(get_annotation_task.annotation_task_begin_time, datetime) else datetime.strptime(get_annotation_task.annotation_task_begin_time, '%Y-%m-%d %H:%M:%S')

    db.session.commit()
    annotation_task_schema = AnnotationTaskSchema()
    annotation_task = annotation_task_schema.dump(get_annotation_task)
    return response_with(resp.SUCCESS_200,value={"annotation_task":annotation_task})

# delete操作
@annotationTasks_bp.route('/<annotation_task_id>', methods=['DELETE'])
def delete_annotation_task_by_id(annotation_task_id):
    get_annotation_task = AnnotationTask.query.get(annotation_task_id)
    db.session.delete(get_annotation_task)
    db.session.commit()
    return make_response({"msg": "ok"}, 204)