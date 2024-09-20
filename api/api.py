import time
from flask import Flask, jsonify,make_response,request,session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import Computed
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from werkzeug.security import check_password_hash,generate_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import json

# 加载 .flaskenv 文件中的环境变量
load_dotenv('.flaskenv')

app = Flask(__name__)

# 配置MySQL数据库URI和禁用事件系统
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DSight:DSight_2024@47.94.128.82:3306/videoAnnotation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


# 生成一个 32 字节的随机密钥
secret_key = os.urandom(32)
# 将密钥编码为 Base64 格式，便于存储和显示
app.secret_key = base64.b64encode(secret_key).decode('utf-8')
# 初始化SQLAlchemy对象
db = SQLAlchemy(app)
migrate = Migrate(app,db) #使用flasjk-migrate自动化完成数据模型到数据库的操作
CORS(app,supports_credentials=True,origins=['http://localhost:9527'])

# 定义一个数据库模型volunteer_
class Volunteer(db.Model):
	__tablename__ = 'volunteers'
	volunteer_id = db.Column(db.Integer)
	volunteer_name = db.Column(db.String(80), nullable=False)
	volunteer_phone_number = db.Column(db.String(80), nullable=False, primary_key=True)
	volunteer_level = db.Column(db.Integer, Computed('((((((floor((volunteer_id / 100000)) + (floor((volunteer_id / 10000)) % 10)) + (floor((volunteer_id / 1000)) % 10)) + (floor((volunteer_id / 100)) % 10)) + (floor((volunteer_id / 10)) % 10)) + (volunteer_id % 10)) % 3)'), nullable=False)
	volunteer_login_pwd = db.Column(db.String(80), nullable=False)

	def create(self):
		db.session.add(self)
		db.session.commit()
		return self
	
	def __repr__(self):
		return f'<Volunteer {self.volunteer_name}>'
	
class VideoInformation(db.Model):
	video_id = db.Column(db.Integer, autoincrement=True)
	create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	video_location = db.Column(db.JSON, nullable=False, primary_key=True)
	video_title = db.Column(db.String(255), nullable=True)
	disaster_type = db.Column(db.Integer, nullable=True)
	disaster_scene = db.Column(db.Integer, nullable=True)
	water_height = db.Column(db.Float, nullable=True)
	water_speed = db.Column(db.Float, nullable=True)
	potential_landmark = db.Column(db.JSON, nullable=True)
	#video_help_information = db.Column(db.String(255), nullable=True)
	video_description = db.Column(db.String(450), nullable=True)
	
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self

class VolunteerSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Volunteer
		sqla_session = db.session
		load_instance = True
		unknown = EXCLUDE  		#忽略未知字段

	volunteer_id =fields.Integer(required=True)
	volunteer_name = fields.String(required = True)
	volunteer_phone_number = fields.String(required = True)
	volunteer_level = fields.Integer()
	volunteer_login_pwd = fields.String(required = True)

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
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return f(*args, **kwargs)
		
#select all操作
@app.route('/volunteers', methods=['GET'])
def get_volunteers():
	volunteers = Volunteer.query.all()
	result = [
		{
			'volunteer_id': volunteer.volunteer_id,
			'volunteer_name': volunteer.volunteer_name,
			'volunteer_phone_number': volunteer.volunteer_phone_number,
			'volunteer_level': volunteer.volunteer_level,
			'volunteer_login_pwd': volunteer.volunteer_login_pwd
		} for volunteer in volunteers
	]
	return jsonify(result)

@app.route('/video/upload', methods=['POST'])
def upload_video():
    data = request.get_json()
    
    # 打印接收到的数据，用于调试
    app.logger.info(f"Received data: {data}")

    # 检查 'video_location' 字段是否存在和是否为有效 JSON 字符串
    if 'video_location' not in data or not data['video_location'].strip():
        app.logger.error('Missing or invalid video_location field')
        return jsonify({'error': 'Missing or invalid video_location'}), 400

    try:
        video_location = json.loads(data['video_location'])
    except json.JSONDecodeError:
        app.logger.error('Invalid JSON format for video_location')
        return jsonify({'error': 'Invalid JSON format for video_location'}), 400

    source_time = None
    if 'sourceTime' in data:
        try:
            source_time = datetime.fromisoformat(data['sourceTime'].replace('Z', '+00:00'))
        except ValueError:
            app.logger.error('Invalid ISO 8601 format for sourceTime')
            return jsonify({'error': 'Invalid ISO 8601 format for sourceTime'}), 400

    collection_time = None
    if 'collectionTime' in data:
        try:
            collection_time = datetime.fromisoformat(data['collectionTime'].replace('Z', '+00:00'))
        except ValueError:
            app.logger.error('Invalid ISO 8601 format for collectionTime')
            return jsonify({'error': 'Invalid ISO 8601 format for collectionTime'}), 400
        
    # 创建一个新的视频信息记录
    new_video = VideoInformation(
        video_location=video_location,
        video_title=data.get('title'),
        disaster_type=data.get('disasterType'),
        disaster_scene=data.get('scene'),
        #emergency_level=data.get('emergencyLevel'),
        #message=data.get('message'),
        create_time=source_time,
        #location=data.get('location'),
        #collection_time=collection_time,
        #collector=data.get('collector'),
        potential_landmark=None  # 假设这个字段是可选的
    )
    
    # 将记录添加到数据库
    new_video.create()  # 使用定义在模型中的方法来添加和提交记录
    
    # 返回成功响应
    return jsonify({'message': 'Video information uploaded successfully!', 'video_id': new_video.video_id}), 201

@app.route('/user/login', methods=['POST'])
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
		
@app.route('/user/info', methods=['GET'])
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
        'name': volunteer.volunteer_name if volunteer.volunteer_name else 'N/A',
        'avatar': '',  # 假设没有 avatar 字段
        'introduction': ''  # 假设没有 introduction 字段
    }

    return jsonify({"code": 20000, "data": volunteer_data})

@app.route('/user/logout', methods=['POST'])  # 修改为 POST 方法
def logout():
    session.pop('user_id', None)  # 从 session 中移除 user_id
    return jsonify({"code": 20000, "data": "success"}), 200

#select_by_id操作
@app.route('/volunteers/<int:volunteer_id>',methods=['GET'])
def get_volunteer_by_id(volunteer_id):
	get_volunteer = Volunteer.query.get(volunteer_id)
	volunteer_schema = VolunteerSchema()
	volunteer = volunteer_schema.dump(get_volunteer)
	return make_response(jsonify({"volunteer":volunteer}))

#insert操作
@app.route('/volunteers',methods=['POST'])
def create_volunteer():
	data = request.get_json()
	volunteer_schema = VolunteerSchema()
	volunteer = volunteer_schema.load(data, session=db.session)  # 确保返回的是 Volunteer 实例
	#volunteer.create()  # 调用 create 方法保存到数据库
	db.session.add(volunteer)  # 直接使用 SQLAlchemy 的会话方法保存到数据库
	db.session.commit()
	result = volunteer_schema.dump(volunteer)
	return make_response(jsonify({"volunteer": result}), 201)

#update操作
@app.route('/volunteers/<volunteer_id>',methods=['PUT'])
def update_volunteer_by_id(volunteer_id):
	data = request.get_json()
	get_volunteer = Volunteer.query.get(volunteer_id)
	if not get_volunteer:
		return jsonify({"error": "Volunteer not found"}), 40
	if data.get('volunteer_name'):
		get_volunteer.volunteer_name = data['volunteer_name']

	if data.get('volunteer_phone_number'):
		get_volunteer.volunteer_phone_number = data['volunteer_phone_number']

	if data.get('volunteer_login_pwd'):
		get_volunteer.volunteer_login_pwd = data['volunteer_login_pwd']

	db.session.add(get_volunteer)
	db.session.commit()
	volunteer_schema = VolunteerSchema(only=['volunteer_id','volunteer_name','volunteer_phone_number','volunteer_login_pwd'])
	volunteer =volunteer_schema.dump(get_volunteer)
	return jsonify({"message": "Volunteer updated successfully"}), 200
	

#delete操作
@app.route('/volunteers/<volunteer_id>',methods=['DELETE'])
def delete_volunteer_by_id(volunteer_id):
	get_volunteer = Volunteer.query.get(volunteer_id)
	db.session.delete(get_volunteer)
	db.session.commit()
	return make_response({"msg":"ok"},204)

@app.before_request
def test_db_connection():
	if not hasattr(app, 'db_checked'):
		try:
			# 尝试执行一个简单的查询
			db.session.execute('SELECT 1')
			print("数据库连接成功")
			app.db_checked = True
		except Exception as e:
			print(f"数据库连接失败: {e}")
			app.db_checked = False

@app.route('/time')
def get_current_time():
	return {'time': time.time()}

@app.route('/')
def print_info():
	print('DSight')
	return jsonify('Fighting!')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=3389)



