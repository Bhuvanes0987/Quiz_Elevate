import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)



@app.get("/users")
def get_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE is_active = 1")
        users = cursor.fetchall()
        db.close()

        return jsonify({"success": True, "users": users})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.get("/users/<int:user_id>")
def get_user(user_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        db.close()

        if user:
            return jsonify({"success": True, "user": user})
        return jsonify({"success": False, "message": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.post("/users")
def add_user():
    try:
        data = request.json
        required_fields = ["name", "student_Class", "school_name", "school_code", "email", "password"]

        for field in required_fields:
            if field not in data or data[field] == "":
                return jsonify({"success": False, "message": f"{field} is required"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users 
            (name, student_Class, school_name, school_code, email, password, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["name"], data["student_Class"], data["school_name"],
            data["school_code"], data["email"], data["password"], "system"
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "User added successfully"})

    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": str(err)}), 500



def update_user(user_id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "User not found"}), 404

        query = """
            UPDATE users SET 
                name = %s,
                student_Class = %s,
                school_name = %s,
                school_code = %s,
                email = %s,
                password = %s,
                updated_by = %s
            WHERE id = %s
        """

        cursor.execute(query, (
            data.get("name"),
            data.get("student_Class"),
            data.get("school_name"),
            data.get("school_code"),
            data.get("email"),
            data.get("password"),
            "system",
            user_id
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "User updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("UPDATE users SET is_active = 0 WHERE id = %s", (user_id,))
        db.commit()
        db.close()

        return jsonify({"success": True, "message": "User deleted successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
