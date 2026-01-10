import os
from flask import Blueprint, request, jsonify, session, render_template, current_app, url_for
from werkzeug.utils import secure_filename
from models import db, User, Vehicle, Location

admin_routes = Blueprint("admin_routes", __name__)


def get_image_url(image_name):
    if not image_name: return None
    if image_name.startswith(('http://', 'https://')): return image_name
    return url_for('static', filename='uploads/' + image_name, _external=True)


def admin_required():
    if "user_id" not in session:
        return jsonify({"error": "Morate biti ulogovani."}), 401
    user = User.query.filter_by(user_id=session["user_id"]).first()
    if not user or user.is_admin != 1:
        return jsonify({"error": "Nemate privilegije admina."}), 403
    return user


@admin_routes.route("/admin/locations/<int:location_id>", methods=["GET"])
def get_admin_location_detail(location_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    
    loc = Location.query.get(location_id)
    if not loc:
        return jsonify({"error": "Lokacija nije pronađena."}), 404
        
    return jsonify({
        "location": {
            "location_id": loc.location_id,
            "location_name": loc.location_name,
            "location_coordinates": loc.location_coordinates,
            "free_locations": loc.free_locations,
            "used_location": loc.used_location,
            "location_map_pic": loc.location_map_pic,
            "location_desc_pic": loc.location_desc_pic,
            "map_url": get_image_url(loc.location_map_pic),
            "desc_url": get_image_url(loc.location_desc_pic)
        }
    }), 200


@admin_routes.route("/admin/locations/<int:location_id>", methods=["PUT"])
def update_location(location_id):
    res = admin_required()
    if isinstance(res, tuple): return res

    loc = Location.query.get(location_id)
    if not loc: return jsonify({"error": "Lokacija nije pronađena."}), 404

    name = request.form.get("location_name")
    coords = request.form.get("location_coordinates")
    free_spots = request.form.get("free_locations")

    if not name or not coords:
        return jsonify({"error": "Naziv i koordinate su obavezni."}), 400

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    def handle_image(file_key, url_key, current_val):
        
        if file_key in request.files:
            file = request.files[file_key]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                return filename
        
      
        new_url = request.form.get(url_key)
        if new_url and new_url.strip() != "":
            return new_url
            
       
        return current_val

    loc.location_name = name
    loc.location_coordinates = coords
    loc.free_locations = int(free_spots)
    
    loc.location_map_pic = handle_image('file_map_pic', 'url_map_pic', loc.location_map_pic)
    loc.location_desc_pic = handle_image('file_desc_pic', 'url_desc_pic', loc.location_desc_pic)

    db.session.commit()
    return jsonify({"message": "Lokacija ažurirana."}), 200


@admin_routes.route("/admin/locations", methods=["POST"])
def add_location():
    res = admin_required()
    if isinstance(res, tuple): return res

    location_name = request.form.get("location_name")
    location_coordinates = request.form.get("location_coordinates")
    
    if not location_name or not location_coordinates:
        return jsonify({"error": "Naziv i koordinate su obavezni."}), 400

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    def handle_image(file_key, url_key):
        if file_key in request.files:
            file = request.files[file_key]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                return filename
        return request.form.get(url_key)

    new_location = Location(
        location_name=location_name,
        location_coordinates=location_coordinates,
        free_locations=int(request.form.get("free_locations", 0)),
        used_location=int(request.form.get("used_location", 0)),
        location_map_pic=handle_image('file_map_pic', 'url_map_pic'),
        location_desc_pic=handle_image('file_desc_pic', 'url_desc_pic')
    )

    db.session.add(new_location)
    db.session.commit()
    return jsonify({"message": "Lokacija uspješno dodana.", "location_id": new_location.location_id}), 201


@admin_routes.route("/admin/users", methods=["GET"])
def list_users():
    res = admin_required()
    if isinstance(res, tuple): return res
    users = User.query.all()
    user_list = [{"user_id": u.user_id, "username": u.username, "email": u.email, "first_name": u.first_name, "last_name": u.last_name, "phone": u.phone, "is_admin": u.is_admin} for u in users]
    return jsonify({"users": user_list}), 200

@admin_routes.route("/admin/locations", methods=["GET"])
def list_locations():
    res = admin_required()
    if isinstance(res, tuple): return res
    locations = Location.query.all()
    location_list = [{"location_id": loc.location_id, "location_coordinates": loc.location_coordinates, "free_locations": loc.free_locations, "used_location": loc.used_location, "location_map_pic": loc.location_map_pic, "location_desc_pic": loc.location_desc_pic} for loc in locations]
    return jsonify({"locations": location_list}), 200

@admin_routes.route("/admin/locations/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    loc = Location.query.get(location_id)
    if not loc: return jsonify({"error": "Lokacija nije pronađena."}), 404
    from models import Reservation
    Reservation.query.filter_by(location_id=location_id).delete()
    db.session.delete(loc)
    db.session.commit()
    return jsonify({"message": f"Lokacija sa id={location_id} obrisana."}), 200

@admin_routes.route("/admin/vehicles/<int:car_id>", methods=["DELETE"])
def delete_vehicle(car_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    vehicle = Vehicle.query.filter_by(car_id=car_id).first()
    if not vehicle: return jsonify({"error": "Vozilo nije pronađeno."}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vozilo obrisano."}), 200

@admin_routes.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    user = User.query.get(user_id)
    if not user or user.user_id == session["user_id"]: return jsonify({"error": "Nevalidan zahtjev."}), 400
    from models import Reservation, Vehicle, Payment
    Reservation.query.filter_by(user_id=user_id).delete()
    Vehicle.query.filter_by(user_id=user_id).delete()
    Payment.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Korisnik obrisan."}), 200

@admin_routes.route("/admin/vehicles", methods=["GET"])
def list_vehicles():
    res = admin_required()
    if isinstance(res, tuple): return res
    vehicles = Vehicle.query.all()
    vehicle_list = []
    from models import Reservation
    for v in vehicles:
        owner = v.owner
        active_res = Reservation.query.filter_by(vehicle_id=v.car_id).first()
        loc_name = active_res.location.location_coordinates if active_res and active_res.location else "NE"
        vehicle_list.append({"car_id": v.car_id, "owner_name": f"{owner.first_name} {owner.last_name}" if owner else "Nepoznato", "vehicle_type": v.vehicle_type, "vehicle_production_mark": v.vehicle_production_mark, "vehicle_licence_plate": v.vehicle_licence_plate, "parked_location": loc_name})
    return jsonify({"vehicles": vehicle_list}), 200

@admin_routes.route("/admin/add-admin", methods=["POST"])
def add_admin_api():
    res = admin_required()
    if isinstance(res, tuple): return res
    data = request.get_json()
    from werkzeug.security import generate_password_hash
    new_admin = User(first_name=data.get("first_name"), last_name=data.get("last_name"), username=data.get("username"), email=data.get("email"), password=generate_password_hash(data.get("password", "admin123")), phone=data.get("phone"), is_admin=1)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin kreiran."}), 201


@admin_routes.route("/admin/vehicle-details/<int:car_id>", methods=["GET"])
def get_admin_vehicle_details(car_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    
    vehicle = Vehicle.query.get(car_id)
    if not vehicle:
        return jsonify({"error": "Vozilo nije pronađeno."}), 404
        
    owner = vehicle.owner
    from models import Reservation
    
    active_res = Reservation.query.filter_by(vehicle_id=car_id).first()
    
    reservations = Reservation.query.filter_by(vehicle_id=car_id).all()
    res_list = []
    for r in reservations:
        res_list.append({
            "reservation_id": r.reservation_id,
            "location": r.location.location_name if r.location else "Nepoznato",
            "coordinates": r.location.location_coordinates if r.location else "N/A",
            "time_period": r.reservation_time_period,
            "reserved_spot": r.reserved_location
        })

    return jsonify({
        "vehicle": {
            "car_id": vehicle.car_id,
            "type": vehicle.vehicle_type,
            "mark": vehicle.vehicle_production_mark,
            "plate": vehicle.vehicle_licence_plate,
            "color": vehicle.vehicle_color,
            "year": vehicle.vehicle_year_of_production,
            "body": vehicle.vehicle_body_type,
            "is_registered": vehicle.is_registered
        },
        "owner": {
            "id": owner.user_id if owner else None,
            "name": f"{owner.first_name} {owner.last_name}" if owner else "Nepoznato",
            "email": owner.email if owner else "N/A",
            "phone": owner.phone if owner else "N/A"
        },
        "current_location": {
            "name": active_res.location.location_name if active_res and active_res.location else "Nije parkirano",
            "coordinates": active_res.location.location_coordinates if active_res and active_res.location else "N/A",
            "spot": active_res.reserved_location if active_res else "N/A"
        },
        "reservations": res_list
    }), 200



@admin_routes.route("/admin/reservations/all", methods=["GET"]) 
def admin_list_all_reservations():
    res = admin_required()
    if isinstance(res, tuple): return res

    from models import Reservation
    reservations = Reservation.query.all()
    result = []
    for r in reservations:
        u = User.query.get(r.user_id)
        v = Vehicle.query.get(r.vehicle_id)
        l = Location.query.get(r.location_id)
        
        result.append({
            "reservation_id": r.reservation_id,
            "user_name": f"{u.first_name} {u.last_name}" if u else "Nepoznato",
            "username": u.username if u else "N/A",
            "vehicle_plate": v.vehicle_licence_plate if v else "N/A",
            "location_name": l.location_name if l else "N/A",
            "time_period": r.reservation_time_period,
            "reserved_location": r.reserved_location
        })

    return jsonify({"reservations": result}), 200


@admin_routes.route("/admin/reservations/<int:reservation_id>", methods=["DELETE"])
def admin_delete_reservation_api(reservation_id):
    res = admin_required()
    if isinstance(res, tuple): return res

    from models import Reservation
    r = Reservation.query.get(reservation_id)
    if not r:
        return jsonify({"error": "Rezervacija nije pronađena."}), 404


    loc = Location.query.get(r.location_id)
    if loc:
        loc.free_locations += 1
        loc.used_location -= 1

    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": "Rezervacija obrisana."}), 200


@admin_routes.route("/admin/reservations/<int:reservation_id>", methods=["GET"])
def admin_get_reservation_detail(reservation_id):
    res = admin_required()
    if isinstance(res, tuple): return res

    from models import Reservation, Payment
    r = Reservation.query.get(reservation_id)
    if not r:
        return jsonify({"error": "Rezervacija nije pronađena."}), 404

    u = User.query.get(r.user_id)
    v = Vehicle.query.get(r.vehicle_id)
    l = Location.query.get(r.location_id)
    p = Payment.query.get(r.payment_id)

    return jsonify({
        "reservation": {
            "id": r.reservation_id,
            "time_period": r.reservation_time_period,
            "spot": r.reserved_location,
            "user": {
                "id": u.user_id,
                "full_name": f"{u.first_name} {u.last_name}",
                "email": u.email,
                "phone": u.phone
            },
            "vehicle": {
                "id": v.car_id,
                "mark": v.vehicle_production_mark,
                "plate": v.vehicle_licence_plate
            },
            "location": {
                "id": l.location_id,
                "name": l.location_name,
                "coords": l.location_coordinates
            },
            "payment": {
                "id": p.payment_id,
                "type": p.payment_method 
            }
        }
    }), 200


@admin_routes.route("/admin/user-details/<int:user_id>", methods=["GET"])
def get_user_details_full(user_id):
    res = admin_required()
    if isinstance(res, tuple): return res
    
    user = User.query.get(user_id)
    if not user: return jsonify({"error": "Nema korisnika"}), 404
    
    from models import Reservation, Vehicle, Payment, TicketSlip
    
   
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    v_list = [{
        "mark": v.vehicle_production_mark,
        "type": v.vehicle_type,
        "plate": v.vehicle_licence_plate,
        "color": v.vehicle_color,
        "year": v.vehicle_year_of_production,
        "body_type": v.vehicle_body_type,
        "registered": v.is_registered
    } for v in vehicles]
    
 
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    r_list = [{
        "location": r.location.location_name if r.location else "N/A",
        "period": r.reservation_time_period,
        "start": "N/A", 
        "end": "N/A",
        "spot": r.reserved_location
    } for r in reservations]
    
  
    payments = Payment.query.filter_by(user_id=user_id).all()
    p_list = [{
        "method": p.payment_method,
        "paypal": p.paypal_email if hasattr(p, 'paypal_email') else "N/A",
        "last_4": p.card_number[-4:] if p.card_number else "****",
        "holder": p.card_holder_name if hasattr(p, 'card_holder_name') else "N/A"
    } for p in payments]

 
    ticket = TicketSlip.query.filter_by(user_id=user_id).first()

    return jsonify({
        "user_info": {
            "id": user.user_id,
            "name": f"{user.first_name} {user.last_name}",
            "username": user.username,
            "email": user.email,
            "phone": user.phone or "Nije uneseno",
            "is_admin": "DA" if user.is_admin == 1 else "NE",
            "has_ticket": "DA" if ticket else "NE"
        },
        "vehicles": v_list,
        "reservations": r_list,
        "payments": p_list
    }), 200