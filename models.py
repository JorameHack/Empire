from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Crée une instance SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)  # Prénom
    last_name = db.Column(db.String(100), nullable=False)   # Nom
    phone_number = db.Column(db.String(15), nullable=False) # Numéro de téléphone
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nom d'utilisateur
    password_hash = db.Column(db.String(128), nullable=False)  # Mot de passe hashé
    balance = db.Column(db.Float, default=0.0)  # Solde initial

    def set_password(self, password):
        """Hash le mot de passe et le stocke."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe donné correspond au mot de passe stocké."""
        return check_password_hash(self.password_hash, password)
