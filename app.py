from flask import Flask, render_template, redirect, session
from flask_cors import CORS
from flask_session import Session
from config import Config
from models import db, Reservation  
from datetime import timedelta
from routes.user_routes import user_routes
from routes.vehicles_routes import vehicles_routes
from routes.location_routes import location_routes
from routes.admin_routes import admin_routes
from routes.reservation_routes import reservation_routes
from routes.slip_ticket_routes import slip_ticket_routes
from routes.static_routes import static_routes
from routes.payments_routes import payments_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

   
    db.init_app(app)

   
    Session(app)
    app.permanent_session_lifetime = timedelta(days=7)

   
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173"],  
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

  
    app.register_blueprint(user_routes, url_prefix="/api/users")
    app.register_blueprint(vehicles_routes)
    app.register_blueprint(location_routes, url_prefix="/api")
    app.register_blueprint(admin_routes, url_prefix="/api")
    app.register_blueprint(reservation_routes, url_prefix="/api")
    app.register_blueprint(slip_ticket_routes, url_prefix="/api")
    app.register_blueprint(static_routes)
    app.register_blueprint(payments_routes)

  
    @app.route("/")
    def home():
        return render_template("home_page.html")

    
    @app.route("/register", methods=["GET"])
    @app.route("/register_page", methods=["GET"])
    def register_page_root():
        return render_template("register_page.html")

    
    @app.route("/login", methods=["GET"])
    @app.route("/login_page", methods=["GET"])
    def login_page_root():
        return render_template("login_page.html")

    
    @app.route("/forgot_password", methods=["GET"])
    def forgot_password_page():
        return render_template("forgot_password.html")

  
    @app.route("/logout", methods=["GET"])
    def logout_root():
        session.clear()
        return redirect("/")

 
    @app.route("/locations", methods=["GET"])
    def locations_page():
        return render_template("locations_page.html")


    @app.route("/locations/details/<int:location_id>", methods=["GET"])
    def location_details_page(location_id):
        return render_template("location_details.html")

  
    @app.route("/reservation_checkout/<int:location_id>", methods=["GET"])
    def reservation_checkout_page(location_id):
        return render_template("reservation_checkout.html")

  
    @app.route("/my_reservations")
    def my_reservations_page():
        if "user_id" not in session:
            return redirect("/login")
        user_reservations = Reservation.query.filter_by(user_id=session["user_id"]).all()
        return render_template("reservations_page.html", reservations=user_reservations)


    @app.route("/admin_users")
    def admin_users_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_show_users.html")

   
    @app.route("/admin/add-admin")
    def add_admin_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_add_admin.html")


    @app.route("/admin_vehicles")
    def admin_vehicles_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_show_vehicles.html")
    
    @app.route("/admin_user_info/<int:user_id>")
    def admin_user_info_page(user_id):
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_user_profile.html", user_id=user_id)


    @app.route("/admin_locations")
    def admin_locations_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_locations.html")


    @app.route("/admin/add_location")
    def admin_add_location_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_add_location.html")
    
  
    @app.route("/admin/location-details/<int:location_id>")
    def admin_location_details_page(location_id):
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_location_details.html", location_id=location_id)

 
    @app.route("/admin_vehicle/<int:car_id>")
    def admin_vehicle_info_page(car_id):
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_vehicle_details.html", car_id=car_id)

 
    @app.route("/admin_reservations")
    def admin_reservations_page():
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_reservations.html")

    @app.route("/admin_reservation_info/<int:res_id>")
    def admin_reservation_info_page(res_id):
        if "user_id" not in session or session.get("is_admin") != 1:
            return redirect("/")
        return render_template("admin_reservation_details.html", res_id=res_id)

    @app.route("/user_profile")
    def profile_page():
        if "user_id" not in session:
            return redirect("/login")
        return render_template("user_profile.html")

   
    @app.route("/reservations_details/<int:res_id>")
    def reservation_details_page(res_id):
        if "user_id" not in session:
            return redirect("/login")
        return render_template("reservations_user_details.html", reservation_id=res_id)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)