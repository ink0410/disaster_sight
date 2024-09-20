import os
import logging
from dotenv import load_dotenv

#数据库连接 URI，日志的级别和目录。项目日后功能涉及的配置代码
basedir = os.path.abspath(os.path.dirname(__file__))

#load env
load_dotenv(os.path.join(basedir,'.flaskenv'))

#load dir
log_dir = os.path.join(basedir,os.getenv('LOG_DIR','logs'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://DSight:DSight_2024@47.94.128.82:3306/videoAnnotation'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')  # 从环境变量加载密钥
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = logging.INFO
    