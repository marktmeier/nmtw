import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for

# Load environment variables
load_dotenv()
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
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///skincare.db")
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


@app.route("/quiz", methods=["GET"])
def quiz():
    """Baumann skin type quiz with Turkish city selection"""
    from baumann import BAUMANN_QUIZ, TURKISH_CITIES
    return render_template("quiz.html", questions=BAUMANN_QUIZ, cities=TURKISH_CITIES)


@app.route("/quiz/result", methods=["POST"])
def quiz_result():
    """Process quiz and show results with weather-adjusted skin type"""
    from baumann import (
        calculate_baumann_from_quiz, 
        apply_weather_modifier, 
        get_skincare_priorities,
        WeatherData,
        TURKISH_CITIES
    )
    from weather import get_weather_data
    
    try:
        # Collect quiz answers
        answers = {}
        for i in range(1, 7):
            q_key = f"q{i}"
            if q_key in request.form:
                answers[i] = int(request.form[q_key])
        
        # Get selected city
        city = request.form.get("city", "istanbul")
        city_data = TURKISH_CITIES.get(city, TURKISH_CITIES["istanbul"])
        
        # Calculate base Baumann score
        base_score = calculate_baumann_from_quiz(answers)
        
        # Get real weather data for the city (or use defaults)
        weather_data = None
        lat = request.form.get("latitude")
        lon = request.form.get("longitude")
        
        if lat and lon:
            weather_data = get_weather_data(lat, lon)
        
        # If no real weather, use city defaults
        if not weather_data:
            weather_data = {
                "temperature": city_data.get("avg_temp_summer", 25),
                "humidity": city_data.get("avg_humidity", 60),
                "uv_index": 5,
                "location": {"city": city_data["name"], "country": "Türkiye"}
            }
        
        # Create WeatherData object
        weather = WeatherData(
            humidity=weather_data.get("humidity", 60),
            temperature=weather_data.get("temperature", 20),
            uv_index=weather_data.get("uv_index", 5),
            city=city
        )
        
        # Apply weather modifier to get adjusted score
        adjusted_score = apply_weather_modifier(base_score, weather)
        
        # Get skincare priorities
        priorities = get_skincare_priorities(adjusted_score, weather)
        
        return render_template("quiz_result.html",
            base_score=base_score,
            adjusted_score=adjusted_score,
            weather=weather_data,
            city=city_data,
            priorities=priorities
        )
        
    except Exception as e:
        logger.error(f"Quiz error: {str(e)}", exc_info=True)
        flash("Bir hata oluştu. Lütfen tekrar deneyin.", "error")
        return redirect(url_for("quiz"))

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

@app.route("/routine-builder")
def routine_builder():
    """Drag and drop routine builder (TODO: implement)"""
    return render_template("routine_builder.html")


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