from flask import Blueprint, render_template


static_routes = Blueprint("static_routes", __name__)


@static_routes.route("/")
@static_routes.route("/home")
def home_page():
    return render_template("home_page.html")



@static_routes.route("/faq")
def faq_page():
    return render_template("faq_page.html")



@static_routes.route("/contact")
def contact_page():
    return render_template("contact_page.html")


@static_routes.route("/privacy_policy")
def privacy_page():
    return render_template("privacy_policy.html")
