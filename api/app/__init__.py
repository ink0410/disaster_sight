import base64
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config, log_dir
from app.utils.log import DayRotatingHandler
from app.utils import responses as resp
from app.utils.responses import response_with
from flask_jwt_extended import JWTManager  # 在顶部导入
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
jwt = JWTManager()  # 与db放在一起
cors = CORS()
migrate = Migrate()
marshmallow = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__,static_folder='../../dist',template_folder="../../dist", static_url_path='/')
    app.config.from_object(config_class)
    #设置secret_key
    secret_key = os.urandom(32)
    app.secret_key = base64.b64encode(secret_key).decode('utf-8')
     # 注册插件
    register_plugins(app)


    # 注册蓝图
    register_blueprints(app)

    # 注册日志处理器
    register_logging(app)

    # 注册错误处理函数
    register_errors(app)

    app.logger.info('Flask Rest Api startup')
    return app

def register_logging(app):
    app.logger.name = 'flask_api'
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    cls_handler = logging.StreamHandler()
    log_file = os.path.join(log_dir, datetime.date.today().strftime("%Y-%m-%d.log"))
    file_handler = DayRotatingHandler(log_file, mode="a", encoding="utf-8")

    logging.basicConfig(level=log_level,
                        format="%(asctime)s %(name)s "
                               "%(filename)s[%(lineno)d] %(funcName)s() %(levelname)s: %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        handlers=[cls_handler, file_handler])

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(os.path.join(log_dir, 'flask_api.log'),maxBytes=1024 * 1024 * 50, backupCount=5, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(name)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))

            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)


def register_plugins(app):
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)
    marshmallow.init_app(app)
    migrate.init_app(app, db)
    


def register_blueprints(app):

    from app.videos import videos_bp
    app.register_blueprint(videos_bp,url_prefix='/videos')

    from app.volunteers import volunteers_bp
    app.register_blueprint(volunteers_bp,url_prefix='/user')

    from app.annotationTasks import annotationTasks_bp
    app.register_blueprint(annotationTasks_bp,url_prefix='/annotationTasks')

    from app.mapView import mapView_bp
    app.register_blueprint(mapView_bp,url_prefix='/mapView')

    from app.uploadTasks import uploadTasks_bp
    app.register_blueprint(uploadTasks_bp,url_prefix='/uploadTasks')

    from app.videoInformation import videoInformation_bp
    app.register_blueprint(videoInformation_bp,url_prefix='/videoInformation')
    swaggerui_blueprint = get_swaggerui_blueprint('/docs','/spec',config={'app_name':'Flask API Docs'})
    app.register_blueprint(swaggerui_blueprint,url_prefix='/docs')



def register_errors(app):

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)