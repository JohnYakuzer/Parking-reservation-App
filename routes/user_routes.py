from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Vehicle, Reservation, Payment, Location, TicketSlip

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/@me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Niste ulogovani"}), 401
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "Korisnik ne postoji"}), 404
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }), 200


@user_routes.route("/profile-details", methods=["GET"])
def get_my_profile_details():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Niste ulogovani"}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Korisnik nije pronađen."}), 404

   
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    v_list = [{
        "mark": v.vehicle_production_mark,
        "type": v.vehicle_type,
        "plate": v.vehicle_licence_plate,
        "color": v.vehicle_color,
        "year": v.vehicle_year_of_production,
        "body_type": v.vehicle_body_type,
        "registered": "DA" if v.is_registered else "NE"
    } for v in vehicles]

   
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    r_list = []
    for r in reservations:
        loc = Location.query.get(r.location_id)
        r_list.append({
            "location": loc.location_name if loc else "Nepoznato",
            "period": r.reservation_time_period,
            "spot": r.reserved_location
        })

   
    payments = Payment.query.filter_by(user_id=user_id).all()
    p_list = [{
        "method": "Kartica" if p.payment_method == "A" else "PayPal",
        "holder": p.card_holder_name or "N/A",
        "last_4": f"**** {p.card_number[-4:]}" if p.card_number else "****",
        "address": p.billing_address_1 or "N/A",
        "paypal": p.paypall_email or "N/A"
    } for p in payments]

    
    ticket = TicketSlip.query.filter_by(user_id=user_id).first()

    return jsonify({
        "user_info": {
            "id": user.user_id,
            "name": f"{user.first_name} {user.last_name}",
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "is_admin": "DA" if user.is_admin == 1 else "NE",
            "has_ticket": "AKTIVNA" if ticket else "NEMA"
        },
        "vehicles": v_list,
        "reservations": r_list,
        "payments": p_list
    }), 200


@user_routes.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "username", "email", "password", "phone"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Polje '{field}' je obavezno."}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Korisnik sa ovim email-om već postoji."}), 409
    if User.query.filter_by(phone=data["phone"]).first():
        return jsonify({"error": "Korisnik sa ovim brojem telefona već postoji."}), 409
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Korisnik sa ovim username-om već postoji."}), 409

    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Korisnik uspješno registrovan.", "user_id": new_user.user_id}), 201


@user_routes.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username_or_email = data.get("username") or data.get("email")
    password = data.get("password")
    if not username_or_email or not password:
        return jsonify({"error": "Username/email i password su obavezni."}), 400

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Pogrešan username/email ili password."}), 401

    session["user_id"] = user.user_id
    session["username"] = user.username
    session["is_admin"] = user.is_admin
    session.permanent = True
    return jsonify({
        "message": f"Korisnik {user.username} uspješno ulogovan.",
        "user_id": user.user_id,
        "username": user.username,
        "is_admin": user.is_admin
    }), 200


@user_routes.route("/logout", methods=["POST"])
def logout_user():
    session.clear()
    return jsonify({"message": "Korisnik uspješno odlogovan."}), 200


@user_routes.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    phone = data.get("phone")
    new_password = data.get("new_password")
    if not email or not phone or not new_password:
        return jsonify({"error": "Email, phone i novi password su obavezni."}), 400

    user = User.query.filter_by(email=email, phone=phone).first()
    if not user:
        return jsonify({"error": "Korisnik sa datim email-om i brojem telefona ne postoji."}), 404

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password uspješno promijenjen."}), 200


@user_routes.route("/verify-forgot-password", methods=["POST"])
def verify_forgot_password():
    data = request.get_json()
    email = data.get("email")
    phone = data.get("phone")
    if not email or not phone:
        return jsonify({"error": "Email i broj telefona su obavezni."}), 400
    user = User.query.filter_by(email=email, phone=phone).first()
    if not user:
        return jsonify({"error": "Ne postoji korisnik sa datim email-om i brojem telefona."}), 404
    return jsonify({"message": "Verifikacija uspješna"}), 200

