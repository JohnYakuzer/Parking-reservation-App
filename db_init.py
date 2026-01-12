from app import create_app
from models import db

app = create_app()

def initialize_database():
    with app.app_context():
        print("Kreiranje tabela u bazi podataka...")
        db.create_all()
        print("Baza podataka je uspješno inicijalizovana.")

if __name__ == "__main__":
    initialize_database()
