from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,EXCLUDE
from app.mapView.models import MapView
from geoalchemy2 import Geometry
from app import db

class GeometryField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.desc  # Assuming 'desc' returns a WKT representation of the geometry

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        return 'SRID=4326;' + value  # Assuming the input is a WKT representation

class MapViewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MapView
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE  # 忽略未知字段

    map_video_id = fields.Integer(required=True)
    location = GeometryField(allow_none=True)
    