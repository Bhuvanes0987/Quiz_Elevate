from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

user_classes_bp = Blueprint("user_classes_bp", __name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# -----------------------------------
# GET ALL CLASSES
# -----------------------------------
@user_classes_bp.get("/user-classes")
def get_classes():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, class_name, is_active,
                   created_by, updated_by,
                   created_at, updated_at
            FROM user_classes
            WHERE is_active = 1
            ORDER BY id DESC
        """)

        classes = cursor.fetchall()
        db.close()

        return jsonify({"success": True, "classes": classes})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# GET SINGLE CLASS
# -----------------------------------
@user_classes_bp.get("/user-classes/<int:class_id>")
def get_class(class_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM user_classes
            WHERE id = %s AND is_active = 1
        """, (class_id,))

        class_data = cursor.fetchone()
        db.close()

        if not class_data:
            return jsonify({"success": False, "message": "Class not found"}), 404

        return jsonify({"success": True, "class": class_data})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# CREATE CLASS
# -----------------------------------
@user_classes_bp.post("/user-classes")
def add_class():
    try:
        data = request.json

        if not data.get("className"):
            return jsonify({"success": False, "message": "Class name is required"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO user_classes
            (class_name, created_by)
            VALUES (%s, %s)
        """, (
            data["className"],
            data.get("createdBy", "system")
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Class created successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# UPDATE CLASS
# -----------------------------------
@user_classes_bp.put("/user-classes/<int:class_id>")
def update_class(class_id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM user_classes WHERE id = %s",
            (class_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "Class not found"}), 404

        cursor.execute("""
            UPDATE user_classes SET
                class_name = %s,
                updated_by = %s
            WHERE id = %s
        """, (
            data["className"],
            data.get("updatedBy", "system"),
            class_id
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Class updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# DELETE CLASS (SOFT DELETE)
# -----------------------------------
@user_classes_bp.delete("/user-classes/<int:class_id>")
def delete_class(class_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE user_classes
            SET is_active = 0
            WHERE id = %s
        """, (class_id,))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Class deleted successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
