from flask import Blueprint, request, jsonify, session
from models import db, TicketSlip, User, Payment, Vehicle, Location
from datetime import datetime

slip_ticket_routes = Blueprint("slip_ticket_routes", __name__)


def login_required():
    if "user_id" not in session:
        return jsonify({"error": "Morate biti ulogovani."}), 401
    return None


def admin_required():
    if "user_id" not in session:
        return jsonify({"error": "Morate biti ulogovani."}), 401

    user = User.query.filter_by(user_id=session["user_id"]).first()
    if not user or user.is_admin != 1:
        return jsonify({"error": "Nemate admin privilegije."}), 403

    return user



@slip_ticket_routes.route("/admin/tickets", methods=["POST"])
def admin_create_ticket():
    res = admin_required()
    if isinstance(res, tuple):
        return res

    data = request.get_json()
    required_fields = [
        "user_id",
        "car_id",
        "ticket_price",
        "ticket_reason",
        "ticket_begin_date",
        "ticket_expire_date"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Polje '{field}' je obavezno."}), 400

    user = User.query.filter_by(user_id=data["user_id"]).first()
    if not user:
        return jsonify({"error": "Korisnik ne postoji."}), 404

    vehicle = Vehicle.query.filter_by(car_id=data["car_id"]).first()
    if not vehicle:
        return jsonify({"error": "Vozilo ne postoji."}), 404

    ticket = TicketSlip(
        user_id=data["user_id"],
        car_id=data["car_id"],
        ticket_price=data["ticket_price"],
        ticket_reason=data["ticket_reason"],
        ticket_begin_date=data["ticket_begin_date"],
        ticket_expire_date=data["ticket_expire_date"],
        paid=0
    )

    user.has_ticket = 1
    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "message": "Parking ticket uspješno kreiran.",
        "ticket_id": ticket.ticket_id
    }), 201



@slip_ticket_routes.route("/admin/tickets/<int:ticket_id>", methods=["PUT"])
def admin_edit_ticket(ticket_id):
    res = admin_required()
    if isinstance(res, tuple):
        return res

    ticket = TicketSlip.query.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        return jsonify({"error": "Ticket nije pronađen."}), 404

    data = request.get_json()

    ticket.ticket_price = data.get("ticket_price", ticket.ticket_price)
    ticket.ticket_reason = data.get("ticket_reason", ticket.ticket_reason)
    ticket.ticket_begin_date = data.get("ticket_begin_date", ticket.ticket_begin_date)
    ticket.ticket_expire_date = data.get("ticket_expire_date", ticket.ticket_expire_date)

    db.session.commit()

    return jsonify({"message": "Ticket uspješno ažuriran."}), 200



@slip_ticket_routes.route("/admin/tickets/<int:ticket_id>", methods=["DELETE"])
def admin_delete_ticket(ticket_id):
    res = admin_required()
    if isinstance(res, tuple):
        return res

    ticket = TicketSlip.query.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        return jsonify({"error": "Ticket nije pronađen."}), 404

    user = User.query.filter_by(user_id=ticket.user_id).first()
    if user:
        user.has_ticket = 0

    db.session.delete(ticket)
    db.session.commit()

    return jsonify({"message": "Ticket uspješno obrisan."}), 200



@slip_ticket_routes.route("/admin/tickets", methods=["GET"])
def admin_list_tickets():
    res = admin_required()
    if isinstance(res, tuple):
        return res

    tickets = TicketSlip.query.all()
    result = []

    for t in tickets:
        result.append({
            "ticket_id": t.ticket_id,
            "user_id": t.user_id,
            "car_id": t.car_id,
            "ticket_price": t.ticket_price,
            "ticket_reason": t.ticket_reason,
            "ticket_begin_date": t.ticket_begin_date,
            "ticket_expire_date": t.ticket_expire_date,
            "paid": t.paid
        })

    return jsonify({"tickets": result}), 200



@slip_ticket_routes.route("/tickets/my", methods=["GET"])
def my_tickets():
    err = login_required()
    if err:
        return err

    tickets = TicketSlip.query.filter_by(user_id=session["user_id"]).all()
    result = []

    for t in tickets:
        result.append({
            "ticket_id": t.ticket_id,
            "car_id": t.car_id,
            "ticket_price": t.ticket_price,
            "ticket_reason": t.ticket_reason,
            "ticket_begin_date": t.ticket_begin_date,
            "ticket_expire_date": t.ticket_expire_date,
            "paid": t.paid
        })

    return jsonify({"tickets": result}), 200



@slip_ticket_routes.route("/tickets/<int:ticket_id>", methods=["GET"])
def ticket_detail(ticket_id):
    err = login_required()
    if err:
        return err

    ticket = TicketSlip.query.filter_by(
        ticket_id=ticket_id,
        user_id=session["user_id"]
    ).first()

    if not ticket:
        return jsonify({"error": "Ticket nije pronađen."}), 404

    return jsonify({
        "ticket": {
            "ticket_id": ticket.ticket_id,
            "car_id": ticket.car_id,
            "ticket_price": ticket.ticket_price,
            "ticket_reason": ticket.ticket_reason,
            "ticket_begin_date": ticket.ticket_begin_date,
            "ticket_expire_date": ticket.ticket_expire_date,
            "paid": ticket.paid
        }
    }), 200



@slip_ticket_routes.route("/tickets/<int:ticket_id>/pay", methods=["POST"])
def pay_ticket(ticket_id):
    err = login_required()
    if err:
        return err

    ticket = TicketSlip.query.filter_by(
        ticket_id=ticket_id,
        user_id=session["user_id"]
    ).first()

    if not ticket:
        return jsonify({"error": "Ticket nije pronađen."}), 404

    if ticket.paid == 1:
        return jsonify({"error": "Ticket je već plaćen."}), 400

    data = request.get_json()
    payment_method = data.get("payment_method")

    if payment_method not in ["A", "B", "C"]:
        return jsonify({"error": "Nevažeći payment_method (A, B, C)."}), 400

    payment = Payment(
        user_id=session["user_id"],
        ticket_id=ticket.ticket_id,
        payment_method=payment_method,
        payment_first_name=data.get("payment_first_name"),
        payment_last_name=data.get("payment_last_name"),
        billing_address_1=data.get("billing_address_1"),
        billing_address_2=data.get("billing_address_2"),
        card_holder_name=data.get("card_holder_name"),
        card_number=data.get("card_number"),
        exp_date=data.get("exp_date"),
        security_code=data.get("security_code"),
        paypall_email=data.get("paypall_email"),
        paypall_password=data.get("paypall_password"),
        save_payment_method=data.get("save_payment_method", 0)
    )

    ticket.paid = 1

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "message": "Ticket uspješno plaćen.",
        "ticket_id": ticket.ticket_id
    }), 200
