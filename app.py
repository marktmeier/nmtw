import os
from flask import Flask, render_template, request, flash, redirect, url_for
from weather import get_weather_data
from skincare import generate_routine

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get form data
        skin_type = request.form.get("skin_type")
        sensitivity = request.form.get("sensitivity")
        concerns = request.form.getlist("concerns")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not all([skin_type, sensitivity, latitude, longitude]):
            flash("Please fill in all required fields", "error")
            return redirect(url_for("index"))

        # Get weather data
        weather_data = get_weather_data(latitude, longitude)
        if not weather_data:
            flash("Unable to fetch weather data. Please try again.", "error")
            return redirect(url_for("index"))

        # Generate skincare routine
        routine = generate_routine(skin_type, sensitivity, concerns, weather_data)

        return render_template("results.html",
                             routine=routine,
                             weather=weather_data,
                             skin_type=skin_type)

    except Exception as e:
        app.logger.error(f"Error generating recommendation: {str(e)}")
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("index"))
