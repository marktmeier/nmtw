from app import db
from datetime import datetime

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
