from flask import request,jsonify,session
from flask_jwt_extended import create_access_token,decode_token
from app import db
from app.volunteers import volunteers_bp
from app.volunteers.models import Volunteer
from app.volunteers.schema import VolunteerSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from functools import wraps
from config import Config
from datetime import datetime, timedelta
import traceback  # 导入 traceback 模块
import jwt

def generate_token(phone_number):
    exp = datetime.utcnow() + timedelta(seconds=1800)  # Token 有效期，例如25 分钟
    token = jwt.encode({'user_id': phone_number, 'exp': exp}, 'secret', algorithm='HS256')
    print(f"Token generated for phone {phone_number}: {token}")  # 调试生成的 token 内容
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # 或从其他地方获取 token
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, Config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return f(*args, **kwargs)
		

@volunteers_bp.route('/register', methods=['POST'])
def create_volunteers():
    """
    用户注册接口
    ---
    parameters:
        - in: body
          name: body
          schema:
            required:
                - volunteer_phone_number
                - volunteer_login_pwd
            properties:
                volunteer_phone_number:
                    type: string
                    description: 用户联系方式
                    default: ""
                volunteer_login_pwd:
                    type: string
                    description: 用户密码
                    default: ""
    responses:
        201:
            description: 注册成功
            schema:
                properties:
                    code:
                        type: string
        422:
            description: 注册失败
            schema:
                properties:
                    code:
                        type: string
                    message:
                        type: string
    """
    try:
        data = request.get_json()
        print(data)
        data['volunteer_login_pwd'] = Volunteer.generate_hash(data['volunteer_login_pwd'])
        volunteer_schema = VolunteerSchema()
        volunteers = volunteer_schema.load(data)
        result = volunteer_schema.dump(volunteers.create())
        return jsonify({"code": 20000, "message": "Logged in successfully"}), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return response_with(resp.INVALID_INPUT_422)

@volunteers_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    volunteer_phone_number = data.get('username')
    volunteer_login_pwd = data.get('password')

    print(f"Received data: {data}")  # 调试输入的数据

    if not volunteer_phone_number or not volunteer_login_pwd:
        print("Missing username or password")  # 调试缺失的用户名或密码
        return jsonify({"code": 60204, "message": "Account and password are incorrect."}), 400

    volunteer = Volunteer.query.filter_by(volunteer_phone_number=volunteer_phone_number).first()
    print(f"Volunteer found: {volunteer}")  # 调试查询到的志愿者信息

    if volunteer and volunteer_login_pwd:
        token = generate_token(volunteer.volunteer_phone_number)  # 生成 token
        session['user_id'] = volunteer.volunteer_phone_number
        print(f"Generated token: {token}")  # 调试生成的 token
        return jsonify({"code": 20000, "message": "Logged in successfully", "data": {"token": token}}), 200
    else:
        print("Invalid volunteer or password")  # 调试无效的志愿者或密码
        return jsonify({"code": 60204, "message": "Account and password are incorrect."}), 401

    

@volunteers_bp.route('/info', methods=['GET'])
def volunteer_info():
    token = request.args.get('token')
    if not token:
        return jsonify({"code": 50008, "message": "Login failed, unable to get user details."}), 401

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.InvalidTokenError:
        return jsonify({"code": 50008, "message": "Invalid token."}), 401
    volunteer = Volunteer.query.get(user_id)
    if not volunteer:
        return jsonify({"code": 50008, "message": "Volunteer not found."}), 404

    # 映射志愿者等级到名称
    level_map = {0: 'admin', 1: 'editor', 2: 'visitor'}
    volunteer_level_name = level_map.get(volunteer.volunteer_level, 'unknown')

    # 构建响应数据结构
    volunteer_data = {
        
        'roles': [volunteer_level_name] if volunteer_level_name != 'unknown' else [],  # 确保roles是列表
        'name': volunteer.volunteer_id if volunteer.volunteer_id else 'N/A',
        #'avatar': '',  # 假设没有 avatar 字段
        #'introduction': ''  # 假设没有 introduction 字段
        'volunteer_id': volunteer.volunteer_id if volunteer.volunteer_id else 'N/A',
    }
    print(volunteer_data)
    return jsonify({"code": 20000, "data": volunteer_data})

@volunteers_bp.route('/logout', methods=['POST'])  # 修改为 POST 方法
def logout():
    session.pop('user_id', None)  # 从 session 中移除 user_id
    return jsonify({"code": 20000, "data": "success"}), 200