
from flask import Flask, request, jsonify, session, send_from_directory
from functools import wraps
from werkzeug.security import check_password_hash
from database.connection import get_db_connection
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            return jsonify({"message": "Please login first"}), 401

        return function(*args, **kwargs)

    return wrapper



@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")

@app.route("/api/departments", methods=["GET"])
def departments():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM departments ORDER BY id")
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(result)



@app.route("/api/announcements", methods=["GET"])
def announcements():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM announcements
        ORDER BY created_at DESC
    """)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(result)



@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and check_password_hash(user["password_hash"], password):
        session["admin_id"] = user["id"]

        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid username or password"}), 401


@app.route("/api/logout", methods=["POST"])
@admin_required
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})



@app.route("/api/announcements", methods=["POST"])
@admin_required
def add_announcement():
    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO announcements (title, content)
        VALUES (%s, %s)
        """,
        (title, content)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Announcement added successfully"}), 201



@app.route("/api/announcements/<int:id>", methods=["PUT"])
@admin_required
def update_announcement(id):
    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE announcements
        SET title = %s, content = %s
        WHERE id = %s
        """,
        (title, content, id)
    )

    connection.commit()
    updated = cursor.rowcount

    cursor.close()
    connection.close()

    if updated == 0:
        return jsonify({"message": "Announcement not found"}), 404

    return jsonify({"message": "Announcement updated successfully"})



@app.route("/api/announcements/<int:id>", methods=["DELETE"])
@admin_required
def delete_announcement(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM announcements WHERE id = %s",
        (id,)
    )

    connection.commit()
    deleted = cursor.rowcount

    cursor.close()
    connection.close()

    if deleted == 0:
        return jsonify({"message": "Announcement not found"}), 404

    return jsonify({"message": "Announcement deleted successfully"})

@app.route("/<path:filename>")
def frontend_pages(filename):
    return send_from_directory("frontend", filename)  


if __name__ == "__main__":
    app.run(debug=True)
