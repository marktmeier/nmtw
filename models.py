from datetime import datetime
from app import db

class SkinMoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    mood = db.Column(db.String(20), nullable=False)  # e.g., 'happy', 'dry', 'irritated'
    notes = db.Column(db.Text)
    weather_temp = db.Column(db.Float)
    weather_humidity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'mood': self.mood,
            'notes': self.notes,
            'weather_temp': self.weather_temp,
            'weather_humidity': self.weather_humidity,
            'created_at': self.created_at.isoformat()
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'cleanser', 'moisturizer', 'sunscreen'
    skin_types = db.Column(db.String(100), nullable=False)  # comma-separated list: 'oily,combination'
    concerns = db.Column(db.String(200))  # comma-separated list: 'acne,aging'
    ingredients = db.Column(db.Text)
    description = db.Column(db.Text)
    weather_conditions = db.Column(db.String(100))  # e.g., 'humid,dry,hot,cold'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'skin_types': self.skin_types.split(','),
            'concerns': self.concerns.split(',') if self.concerns else [],
            'ingredients': self.ingredients,
            'description': self.description,
            'weather_conditions': self.weather_conditions.split(',') if self.weather_conditions else [],
            'created_at': self.created_at.isoformat()
        }