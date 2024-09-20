from flask import Blueprint
videos_bp = Blueprint('videos_bp',__name__)
from app.videos import routes