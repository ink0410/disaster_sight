from flask import Blueprint, request, jsonify, make_response
from app import db
from app.mapView.models import MapView
from app.mapView.schema import MapViewSchema
from app.mapView import mapView_bp
from app.utils.responses import response_with
from app.utils import responses as resp

#select all
@mapView_bp.route('/', methods=['GET'])
def get_map_views():
	map_views = MapView.query.all()
	map_view_schema = MapViewSchema(many=True)
	result = map_view_schema.dump(map_views)
	return response_with(resp.SUCCESS_200,value={"mapViews":result})

# select_by_id操作
@mapView_bp.route('/<int:map_video_id>',methods=['GET'])
def get_map_view_by_id(map_video_id):
    fetched = MapView.query.get_or_404(map_video_id)
    mapView_schema = MapViewSchema()
    mapView = mapView_schema.dump(fetched)
    return response_with(resp.SUCCESS_200,value={"mapView":mapView})

# insert操作
@mapView_bp.route('/', methods=['POST'])
def create_mapView():
    try:
        data = request.get_json()
        print(data)
        mapView_schema = MapViewSchema()
        mapView = mapView_schema.load(data,session=db.session)
        db.session.add(mapView)
        db.session.commit()
        result = mapView_schema.dump(mapView)
        return response_with(resp.SUCCESS_201,value={"mapView":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# update操作
@mapView_bp.route('/<int:map_video_id>',methods=['PUT'])
def update_mapView_detail(map_video_id):
    data = request.get_json()
    get_map_view = MapView.query.get_or_404(map_video_id)
    if 'location' in data:
        get_map_view.location = 'SRID=4326;' + data['location']  # Assuming the input is a WKT representation

    db.session.add(get_map_view)
    db.session.commit()
    map_view_schema = MapViewSchema()
    return make_response(map_view_schema.jsonify(get_map_view), 200)

# delete操作
@mapView_bp.route('/<int:map_video_id>', methods=['DELETE'])
def delete_map_view(map_video_id):
	map_view = MapView.query.get_or_404(map_video_id)
	db.session.delete(map_view)
	db.session.commit()
	return make_response({"msg": "ok"}, 204)