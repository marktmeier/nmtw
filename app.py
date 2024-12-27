import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from weather import get_weather_data
from skincare import generate_routine

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        logger.debug("Fetching weather data")
        weather_data = get_weather_data(latitude, longitude)
        if not weather_data:
            logger.error("Failed to fetch weather data")
            flash("Unable to fetch weather data. Please try again.", "error")
            return redirect(url_for("index"))

        logger.debug(f"Weather data received: {weather_data}")

        # Generate skincare routine
        logger.debug("Generating skincare routine")
        routine = generate_routine(skin_type, sensitivity, concerns, weather_data)
        logger.debug(f"Generated routine: {routine}")

        return render_template("results.html",
                             routine=routine,
                             weather=weather_data,
                             skin_type=skin_type)

    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}", exc_info=True)
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("index"))