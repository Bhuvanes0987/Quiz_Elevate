from flask import Blueprint, request, jsonify
import mysql.connector
import os
import traceback

bp = Blueprint("signup", __name__, url_prefix="/api")

# Load DB configuration from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@bp.route('/signup', methods=['POST'])
def signup():
    conn = None
    cursor = None

    try:
        data = request.get_json()

        name = data.get('name')
        school_name = data.get('schoolname')
        school_code = data.get('schoolcode')
        email = data.get('email')
        password = data.get('password')   # STORE AS-IS (PLAIN)

        # Validate fields
        if not all([name, school_name, school_code, email, password]):
            return jsonify({"message": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Email already registered"}), 409

        # Insert new user - PASSWORD IS STORED AS ORIGINAL
        insert_query = """
            INSERT INTO users (name, school_name, school_code, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, school_name, school_code, email, password))
        conn.commit()

        return jsonify({"message": "Signup successful!"}), 201

    except Exception as e:
        print("\n❌ SIGNUP ERROR ❌")
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"message": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
