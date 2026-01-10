import os
from datetime import timedelta

class Config:
   
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey123"

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "parking.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = "Content-Type"

    SESSION_TYPE = "filesystem"        
    SESSION_FILE_DIR = os.path.join(BASEDIR, "flask_session")
    SESSION_PERMANENT = True           
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_USE_SIGNER = True          
    SESSION_COOKIE_NAME = "parking_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"    
    SESSION_COOKIE_SECURE = False     
