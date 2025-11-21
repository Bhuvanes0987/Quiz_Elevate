# from flask import Blueprint, request, jsonify
# from werkzeug.security import check_password_hash
# import mysql.connector
# import os


# bp_login = Blueprint('bp_login', __name__)

# DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME"),
#     "port": int(os.getenv("DB_PORT", 3306))
# }

# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

# @bp_login.route('/login', methods=["POST", "OPTIONS"])
# def login():
#     conn = None
#     cursor = None

#     try:
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')

#         if not email or not password:
#             return jsonify({"success": False, "message": "Email and password are required"}), 400

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         # Fetch user by email
#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if not user:
#             return jsonify({"success": False, "message": "Email not found"}), 404

#         # Check hashed password
#         if not check_password_hash(user['password'], password):
#             return jsonify({"success": False, "message": "Invalid password"}), 401

#         return jsonify({
#             "success": True,
#             "message": "Login successful",
#             "user": {
#                 "id": user['id'],
#                 "name": user['name'],
#                 "email": user['email']
#             }
#         }), 200

#     except Exception as e:
#         print("\n❌ LOGIN ERROR ❌")
#         print("Error:", e)
#         return jsonify({"success": False, "message": "Internal server error"}), 500

#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()


from flask import Blueprint, request, jsonify
import mysql.connector
import os

bp_login = Blueprint('bp_login', __name__, url_prefix='/api')

# Load DB config
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@bp_login.route('/login', methods=['POST'])
def login():
    conn = None
    cursor = None

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch user
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "Email not found"}), 404

        # Check plain-text password
        if user['password'] != password:
            return jsonify({"success": False, "message": "Invalid password"}), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:
        print("\n❌ LOGIN ERROR ❌")
        print("Error:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
