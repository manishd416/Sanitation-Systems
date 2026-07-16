from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/awareness")
def awareness():
    return render_template("awareness.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/hazards")
def hazards():
    return render_template("hazards.html")

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        location = request.form["location"]
        complaint = request.form["complaint"]
        image = request.files.get("image")

        filename = ""
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # Ensure table exists (Good practice to include if database.db is fresh)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, mobile TEXT, location TEXT, 
            complaint TEXT, image TEXT, date TEXT, status TEXT
        )
        """)

        cur.execute("""
        INSERT INTO complaints
        (name, mobile, location, complaint, image, date, status)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            name, mobile, location, complaint, filename,
            datetime.now().strftime("%d-%m-%Y"), "Pending"
        ))

        conn.commit()
        conn.close()

        # Fixed: Passing location and complaint to match success.html
        return render_template("success.html", name=name, location=location, issue=complaint)

    return render_template("report.html")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860
    )