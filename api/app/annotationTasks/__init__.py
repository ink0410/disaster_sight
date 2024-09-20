from flask import Blueprint
annotationTasks_bp = Blueprint('annotationTasks_bp',__name__)
from app.annotationTasks import routes