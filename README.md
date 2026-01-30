# No Matter The Weather (NMTW)

Weather-dependent skincare recommendation app that provides personalized skincare advice based on current weather conditions and your skin type.

## Features

- **Skin Type Quiz** - Determine your skin type through an interactive questionnaire
- **Weather Integration** - Real-time weather data via OpenWeather API
- **Geolocation** - Automatic location detection for local weather
- **Mood Tracker** - Track how weather affects your skin and mood
- **Personalized Recommendations** - Skincare advice tailored to weather conditions

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite / PostgreSQL
- **Frontend:** Bootstrap 5, Jinja2 templates
- **APIs:** OpenWeather API

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the app
python main.py
```

The app will be available at `http://localhost:5000`

## License

MIT
