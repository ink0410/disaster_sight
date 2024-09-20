from flask import Blueprint
videoInformation_bp = Blueprint('videoInformation_bp',__name__)
from app.videoInformation import routes