from flask import Blueprint, render_template, request, jsonify, session, redirect
from models import db, Payment


payments_routes = Blueprint("payments_routes", __name__)


@payments_routes.route("/payments", methods=["GET"])
def payments_page():
    if not session.get("user_id"):
        return redirect("/login")  

    user_id = session["user_id"]
    payments = Payment.query.filter_by(user_id=user_id).all()

    return render_template("payments_page.html", payments=payments)



@payments_routes.route("/api/payments/user/@me", methods=["GET"])
def get_user_payments():
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    user_id = session["user_id"]
    payments = Payment.query.filter_by(user_id=user_id).all()

    payment_list = []
    for p in payments:
        payment_list.append({
            "payment_id": getattr(p, "payment_id", getattr(p, "id", None)),
            "payment_method": p.payment_method,
            "card_holder_name": p.card_holder_name,
            "card_number": p.card_number,
            "billing_address_1": p.billing_address_1,
            "paypall_email": p.paypall_email
        })

    return jsonify({"payments": payment_list}), 200



@payments_routes.route("/api/payments/delete/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    if not session.get("user_id"):
        return jsonify({"error": "Niste ulogovani."}), 401

    user_id = session["user_id"]
    payment = Payment.query.filter_by(payment_id=payment_id, user_id=user_id).first()

    if not payment:
        return jsonify({"error": "Payment nije pronađen."}), 404

    db.session.delete(payment)
    db.session.commit()
    return jsonify({"message": "Payment uspješno obrisan."}), 200



@payments_routes.route("/api/payments/add", methods=["POST"])
def add_payment():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Niste ulogovani."}), 401

    data = request.json
    if not data:
        return jsonify({"error": "Nema podataka"}), 400

    method = data.get("payment_method")
    if method not in ["A", "B", "C"]:
        return jsonify({"error": "Nevažeći payment method"}), 400

    payment = Payment(
        user_id=user_id,
        payment_method=method,
        card_holder_name=data.get("card_holder_name"),
        card_number=data.get("card_number"),
        billing_address_1=data.get("billing_address_1"),
        paypall_email=data.get("paypall_email")
    )

    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment uspješno dodan."}), 201



@payments_routes.route("/add_payment", methods=["GET"])
def add_payment_page():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("add_payment.html")



