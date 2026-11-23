
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to our University"


@app.route("/api/departments")
def departments():
    return "List of university departments"


@app.route("/api/announcements")
def announcements():
    return "List of university announcements"


@app.route("/login")
def login():
    return "Admin Login Page"


if __name__ == "__main__":
    app.run(debug=True)
