from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database.db import init_db, save_scan, get_recent_scans, get_stats
from src.detection.message_detector import analyze_message

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    result = None
    message = ""
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            flash("Please enter a message to analyze.", "warning")
        elif len(message) > 10000:
            flash("Please keep the message under 10,000 characters.", "warning")
        else:
            result = analyze_message(message)
            save_scan(message, result)
    return render_template("scanner.html", result=result, message=message)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", stats=get_stats(), scans=get_recent_scans(10))

@app.route("/history")
def history():
    return render_template("history.html", scans=get_recent_scans(100))

@app.route("/safety")
def safety():
    return render_template("safety_guide.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
