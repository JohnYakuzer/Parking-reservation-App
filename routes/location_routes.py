from flask import Blueprint, request, jsonify, session, url_for
from models import db, Location

location_routes = Blueprint("location_routes", __name__)

def get_image_url(image_name):
    if not image_name:
        return None
   
    if image_name.startswith(('http://', 'https://')):
        return image_name
  
    return url_for('static', filename='uploads/' + image_name, _external=True)


@location_routes.route("/locations", methods=["GET"])
def list_locations():
    locations = Location.query.all()
    location_list = []

    for loc in locations:
        location_list.append({
            "location_id": loc.location_id,
            "location_name": loc.location_name or loc.location_coordinates, 
            "location_coordinates": loc.location_coordinates,
            "free_locations": loc.free_locations,
            "used_location": loc.used_location,
            "location_map_pic": get_image_url(loc.location_map_pic),
            "location_desc_pic": get_image_url(loc.location_desc_pic)
        })

    return jsonify({"locations": location_list}), 200



@location_routes.route("/location_detail/<int:location_id>", methods=["GET"])
def location_detail(location_id):
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    loc = Location.query.filter_by(location_id=location_id).first()
    if not loc:
        return jsonify({"error": "Lokacija nije pronađena."}), 404

    location_detail = {
        "location_id": loc.location_id,
        "location_name": loc.location_name or loc.location_coordinates,
        "location_coordinates": loc.location_coordinates,
        "free_locations": loc.free_locations,
        "used_location": loc.used_location,
        "location_map_pic": get_image_url(loc.location_map_pic),
        "location_desc_pic": get_image_url(loc.location_desc_pic),
        "additional_info": "Detalji rezervacija i ostale informacije će biti dodane kasnije."
    }

    return jsonify({"location": location_detail}), 200