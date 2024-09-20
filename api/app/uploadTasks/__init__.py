from flask import Blueprint
uploadTasks_bp = Blueprint('uploadTasks_bp',__name__)
from app.uploadTasks import routes