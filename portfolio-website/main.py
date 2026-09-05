from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/work-experience")
def work_experience():
    return render_template("work-experience.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    sender_email = os.environ.get("EMAIL_ADDRESS")
    sender_password = os.environ.get("EMAIL_PASSWORD")

    email_message = f"""\
Subject: Portfolio Contact Form

Name: {name}
Email: {email}

Message:
{message}
"""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(sender_email, sender_password)
        connection.sendmail(
            sender_email,
            sender_email,
            email_message
        )

    flash("Message successfully sent!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)