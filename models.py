from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.reservation_id"), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket_slips.ticket_id"), nullable=True)

    def __repr__(self):
        return f"<Admin id={self.id} user_id={self.user_id}>"


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin = db.Column(db.Integer, default=0)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(50), nullable=True)

    car_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)
    has_ticket = db.Column(db.Integer, default=0)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket_slips.ticket_id"), nullable=True)

    vehicles = db.relationship("Vehicle", backref="owner", lazy=True, foreign_keys="[Vehicle.user_id]")
    reservations = db.relationship("Reservation", backref="user", lazy=True, foreign_keys="[Reservation.user_id]")
    tickets = db.relationship("TicketSlip", backref="user", lazy=True, foreign_keys="[TicketSlip.user_id]")

    def __repr__(self):
        return f"<User id={self.user_id} username={self.username}>"


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    vehicle_type = db.Column(db.String(255))
    vehicle_production_mark = db.Column(db.String(255))
    vehicle_licence_plate = db.Column(db.String(100))
    vehicle_color = db.Column(db.String(100))
    vehicle_year_of_production = db.Column(db.Integer)
    vehicle_body_type = db.Column(db.String(255))
    is_registered = db.Column(db.Integer, default=1)

    reservations = db.relationship("Reservation", backref="vehicle", lazy=True, foreign_keys="[Reservation.vehicle_id]")
    tickets = db.relationship("TicketSlip", backref="vehicle", lazy=True, foreign_keys="[TicketSlip.car_id]")

    def __repr__(self):
        return f"<Vehicle car_id={self.car_id} plate={self.vehicle_licence_plate}>"


class Location(db.Model):
    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), nullable=True)
    location_coordinates = db.Column(db.String(255))
    free_locations = db.Column(db.Integer, default=0)
    used_location = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    car_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)

    location_map_pic = db.Column(db.String(255), nullable=True)
    location_desc_pic = db.Column(db.String(255), nullable=True)

    soon_available_place = db.Column(db.String(255), nullable=True)

    reservations = db.relationship("Reservation", backref="location", lazy=True, foreign_keys="[Reservation.location_id]")

    def __repr__(self):
        return f"<Location id={self.location_id} name={self.location_name} coords={self.location_coordinates}>"


class Reservation(db.Model):
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)
    
  
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.payment_id"), nullable=True)

    reserved_location = db.Column(db.String(255))
    reservation_time_period = db.Column(db.String(255))

    reservation_begin_date = db.Column(db.String(255), nullable=True)
    reservation_exp_date = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Reservation id={self.reservation_id} user_id={self.user_id} loc={self.location_id}>"


class TicketSlip(db.Model):
    __tablename__ = "ticket_slips"

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    car_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)

    ticket_begin_date = db.Column(db.String(255))
    ticket_expire_date = db.Column(db.String(255))
    ticket_price = db.Column(db.Float)
    ticket_reason = db.Column(db.String(500), nullable=True)
    paid = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Ticket id={self.ticket_id} user={self.user_id} price={self.ticket_price}>"


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket_slips.ticket_id"), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.car_id"), nullable=True)

  
    payment_method = db.Column(db.String(1))

    save_payment_method = db.Column(db.Integer, default=0)

    payment_first_name = db.Column(db.String(255))
    payment_last_name = db.Column(db.String(255))

    billing_address_1 = db.Column(db.String(255))
    billing_address_2 = db.Column(db.String(255), nullable=True)

   
    card_holder_name = db.Column(db.String(255), nullable=True)
    card_number = db.Column(db.String(20), nullable=True)
    exp_date = db.Column(db.String(5), nullable=True)
    security_code = db.Column(db.String(100), nullable=True)

 
    paypall_email = db.Column(db.String(255), nullable=True)
    paypall_password = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Payment id={self.payment_id} method={self.payment_method}>"