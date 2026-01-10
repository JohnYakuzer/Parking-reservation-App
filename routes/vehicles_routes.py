from flask import Blueprint, render_template, request, jsonify, session, redirect
from models import db, Vehicle

vehicles_routes = Blueprint("vehicles_routes", __name__)


@vehicles_routes.route("/vehicles", methods=["GET"])
def vehicles_page():
    if not session.get("user_id"):
        return redirect("/login")
    vehicles = Vehicle.query.filter_by(user_id=session["user_id"]).all()
    return render_template("vehicles_page.html", vehicles=vehicles)


@vehicles_routes.route("/add_vehicle", methods=["GET"])
def add_vehicle_page():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("add_vehicle.html")



@vehicles_routes.route("/api/vehicles/add", methods=["POST"])
def add_vehicle():
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    data = request.json
    if not data:
        return jsonify({"error": "Nema podataka"}), 400

    required_fields = ["vehicle_type", "vehicle_production_mark", "vehicle_licence_plate",
                       "vehicle_color", "vehicle_year_of_production", "vehicle_body_type"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Polje '{field}' je obavezno."}), 400

    try:
        year = int(data.get("vehicle_year_of_production"))
    except ValueError:
        return jsonify({"error": "Godina proizvodnje mora biti broj."}), 400

    vehicle = Vehicle(
        user_id=session["user_id"],
        vehicle_type=data.get("vehicle_type"),
        vehicle_production_mark=data.get("vehicle_production_mark"),
        vehicle_licence_plate=data.get("vehicle_licence_plate"),
        vehicle_color=data.get("vehicle_color"),
        vehicle_year_of_production=year,
        vehicle_body_type=data.get("vehicle_body_type"),
        is_registered=1
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"message": "Vozilo uspješno dodano."}), 201



@vehicles_routes.route("/api/vehicles/delete/<int:car_id>", methods=["DELETE"])
def delete_vehicle(car_id):
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    vehicle = Vehicle.query.filter_by(car_id=car_id, user_id=session["user_id"]).first()
    if not vehicle:
        return jsonify({"error": "Vozilo nije pronađeno."}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vozilo uspješno obrisano."}), 200




@vehicles_routes.route("/api/vehicles/my_vehicles", methods=["GET"])
def get_my_vehicles():
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    user_id = session["user_id"]
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()

    vehicle_list = []
    for v in vehicles:
        vehicle_list.append({
            "car_id": v.car_id,
            "vehicle_type": v.vehicle_type,
            "vehicle_production_mark": v.vehicle_production_mark,
            "vehicle_licence_plate": v.vehicle_licence_plate,
            "vehicle_color": v.vehicle_color,
            "vehicle_year_of_production": v.vehicle_year_of_production,
            "vehicle_body_type": v.vehicle_body_type,
            "is_registered": v.is_registered
        })

    return jsonify({"vehicles": vehicle_list}), 200