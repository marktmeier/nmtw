import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Configure app
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy with custom base
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()


@app.route("/", methods=["GET"])
def index():
    logger.debug("Rendering index page")
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        logger.debug("Processing recommendation request")
        logger.debug(f"Form data received: {request.form}")

        # Get form data
        skin_type = request.form.get("skin_type")
        sensitivity = request.form.get("sensitivity")
        concerns = request.form.getlist("concerns")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        logger.debug(f"Parsed form data - skin_type: {skin_type}, sensitivity: {sensitivity}, "
                    f"concerns: {concerns}, location: ({latitude}, {longitude})")

        if not all([skin_type, sensitivity, latitude, longitude]):
            logger.warning("Missing required fields in form submission")
            flash("Please fill in all required fields", "error")
            return redirect(url_for("index"))

        # Get weather data
        from weather import get_weather_data
        logger.debug("Fetching weather data")
        weather_data = get_weather_data(latitude, longitude)
        if not weather_data:
            logger.error("Failed to fetch weather data")
            flash("Unable to fetch weather data. Please try again.", "error")
            return redirect(url_for("index"))

        logger.debug(f"Weather data received: {weather_data}")

        # Generate skincare routine
        from skincare import generate_routine
        logger.debug("Generating skincare routine")
        routine = generate_routine(skin_type, sensitivity, concerns, weather_data)
        logger.debug(f"Generated routine: {routine}")

        # Get product recommendations for each step in routine
        from recommendations import get_product_recommendations
        product_recommendations = {}
        for step in routine:
            category = step["step"].lower()
            products = get_product_recommendations(
                skin_type=skin_type,
                concerns=concerns,
                weather_data=weather_data,
                category=category
            )
            product_recommendations[category] = products

        return render_template("results.html",
                            routine=routine,
                            weather=weather_data,
                            skin_type=skin_type,
                            product_recommendations=product_recommendations)

    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}", exc_info=True)
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("index"))

@app.route("/mood-tracker")
def mood_tracker():
    logger.debug("Accessing mood tracker page")
    from models import SkinMoodEntry
    mood_entries = SkinMoodEntry.query.order_by(SkinMoodEntry.date.desc()).limit(7).all()
    return render_template("mood_tracker.html", mood_entries=mood_entries)

@app.route("/log-mood", methods=["POST"])
def log_mood():
    try:
        logger.debug("Processing mood log request")
        logger.debug(f"Form data received: {request.form}")

        mood = request.form.get("mood")
        notes = request.form.get("notes")

        if not mood:
            logger.warning("Missing mood in form submission")
            flash("Please select a mood", "error")
            return redirect(url_for("mood_tracker"))

        # Get current weather for the entry
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        from weather import get_weather_data
        weather_data = get_weather_data(latitude, longitude) if latitude and longitude else None

        # Create new mood entry
        from models import SkinMoodEntry
        entry = SkinMoodEntry(
            mood=mood,
            notes=notes,
            weather_temp=weather_data["temperature"] if weather_data else None,
            weather_humidity=weather_data["humidity"] if weather_data else None
        )

        db.session.add(entry)
        db.session.commit()

        logger.debug(f"Successfully logged mood entry: {entry.to_dict()}")
        flash("Successfully logged your skin mood!", "success")

    except Exception as e:
        logger.error(f"Error logging mood: {str(e)}", exc_info=True)
        flash("An error occurred while logging your mood. Please try again.", "error")

    return redirect(url_for("mood_tracker"))