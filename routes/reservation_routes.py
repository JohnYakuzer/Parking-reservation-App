from flask import Blueprint, request, jsonify, session
from models import db, Reservation, Location, Vehicle, Payment, User

reservation_routes = Blueprint("reservation_routes", __name__)


def login_required():
    if "user_id" not in session:
        return None, jsonify({"error": "Niste ulogovani."}), 401
    return session["user_id"], None

def admin_required():
    user_id, err = login_required()
    if err:
        return None, err

    user = User.query.filter_by(user_id=user_id).first()
    if not user or user.is_admin != 1:
        return None, jsonify({"error": "Nemate admin privilegije."}), 403

    return user, None


@reservation_routes.route("/my_reservations", methods=["GET"])
def my_reservations():
    user_id, err = login_required()
    if err:
        return err

    reservations = Reservation.query.filter_by(user_id=user_id).all()
    result = []
    for r in reservations:
        loc = Location.query.get(r.location_id)
        veh = Vehicle.query.get(r.vehicle_id)
        
        result.append({
            "reservation_id": r.reservation_id,
            "location_name": loc.location_name if loc else "Nepoznata lokacija",
            "vehicle_plate": veh.vehicle_licence_plate if veh else "N/A",
            "vehicle_mark": veh.vehicle_production_mark if veh else "N/A",
            "reserved_location": r.reserved_location,
            "reservation_time_period": r.reservation_time_period,
            "begin_date": r.reservation_begin_date if r.reservation_begin_date else "Nije navedeno"
        })

    return jsonify({"reservations": result}), 200


@reservation_routes.route("/reservations/create", methods=["POST"])
def create_reservation():
    user_id, err = login_required()
    if err:
        return err

    data = request.get_json() or {}
    required_fields = ["location_id", "vehicle_id", "payment_id", "reserved_location", "reservation_time_period"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Polje '{field}' je obavezno."}), 400

    existing_res = Reservation.query.filter_by(vehicle_id=data["vehicle_id"]).first()
    if existing_res:
        return jsonify({"error": "Ovo vozilo već ima aktivnu rezervaciju."}), 400

    vehicle = Vehicle.query.filter_by(car_id=data["vehicle_id"], user_id=user_id).first()
    if not vehicle:
        return jsonify({"error": "Vozilo ne postoji."}), 403

    payment = Payment.query.filter_by(payment_id=data["payment_id"], user_id=user_id).first()
    if not payment:
        return jsonify({"error": "Payment metoda ne postoji."}), 403

    location = Location.query.filter_by(location_id=data["location_id"]).first()
    if not location or location.free_locations <= 0:
        return jsonify({"error": "Nema slobodnih mjesta."}), 400

    new_reservation = Reservation(
        user_id=user_id,
        location_id=location.location_id,
        vehicle_id=vehicle.car_id,
        payment_id=payment.payment_id,
        reserved_location=data["reserved_location"],
        reservation_time_period=data["reservation_time_period"],
        reservation_begin_date=data.get("begin_date") 
    )

    location.free_locations -= 1
    location.used_location += 1

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({
        "message": f"Payment je uspješan!",
        "reservation_id": new_reservation.reservation_id
    }), 201


@reservation_routes.route("/reservations/delete/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    user_id, err = login_required()
    if err:
        return err

    reservation = Reservation.query.filter_by(reservation_id=reservation_id, user_id=user_id).first()
    if not reservation:
        return jsonify({"error": "Rezervacija nije pronađena."}), 404

    location = Location.query.filter_by(location_id=reservation.location_id).first()
    if location:
        location.free_locations += 1
        location.used_location -= 1

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Rezervacija je uspješno otkazana."}), 200


@reservation_routes.route("/admin/reservations", methods=["GET"])
def list_all_reservations():
    admin, err = admin_required()
    if err: return err
    reservations = Reservation.query.all()
    result = []
    for r in reservations:
        result.append({
            "reservation_id": r.reservation_id,
            "user_id": r.user_id,
            "reserved_location": r.reserved_location,
            "reservation_time_period": r.reservation_time_period
        })
    return jsonify({"reservations": result}), 200

@reservation_routes.route("/admin/reservations/<int:reservation_id>", methods=["DELETE"])
def admin_delete_reservation(reservation_id):
    admin, err = admin_required()
    if err: return err
    reservation = Reservation.query.get(reservation_id)
    if not reservation: return jsonify({"error": "Nije pronađeno"}), 404

    location = Location.query.get(reservation.location_id)
    if location:
        location.free_locations += 1
        location.used_location -= 1

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Obrisano od strane admina."}), 200




@reservation_routes.route("/reservations/detail/<int:reservation_id>", methods=["GET"])
def get_reservation_detail(reservation_id):
    user_id, err = login_required()
    if err:
        return err

    r = Reservation.query.filter_by(reservation_id=reservation_id, user_id=user_id).first()
    if not r:
        return jsonify({"error": "Rezervacija nije pronađena."}), 404

    loc = Location.query.get(r.location_id)
    veh = Vehicle.query.get(r.vehicle_id)
    pay = Payment.query.get(r.payment_id)

    return jsonify({
        "reservation_id": r.reservation_id,
        "reserved_location": r.reserved_location,
        "reservation_time_period": r.reservation_time_period,
        "begin_date": r.reservation_begin_date or "Nije navedeno",
        "location": {
            "name": loc.location_name if loc else "N/A",
            "coordinates": loc.location_coordinates if loc else "N/A",
            "map_pic": loc.location_map_pic if loc else None
        },
        "vehicle": {
            "mark": veh.vehicle_production_mark if veh else "N/A",
            "plate": veh.vehicle_licence_plate if veh else "N/A",
            "type": veh.vehicle_type if veh else "N/A"
        },
        "payment": {
            "method": "PayPal" if pay and pay.payment_method == "C" else "Kartica",
            "details": pay.paypall_email if pay and pay.payment_method == "C" else (f"**** {pay.card_number[-4:]}" if pay and pay.card_number else "****")
        }
    }), 200