from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

user_classes_bp = Blueprint("user_classes_bp", __name__,url_prefix="/api" )

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
            SELECT 
                uc.id,
                uc.class_name,
                uc.is_active,
                GROUP_CONCAT(cfg.group_name) AS subjects,
                GROUP_CONCAT(cfg.id) AS group_ids
            FROM user_classes uc
            LEFT JOIN user_class_groups ucg 
                ON uc.id = ucg.class_id
            LEFT JOIN custom_field_groups cfg
                ON ucg.group_id = cfg.id
            WHERE uc.is_active = 1
            GROUP BY uc.id
            ORDER BY uc.id DESC
        """)

        classes = cursor.fetchall()

        for c in classes:
            c["subjects"] = c["subjects"].split(",") if c["subjects"] else []
            c["group_ids"] = list(map(int, c["group_ids"].split(","))) if c["group_ids"] else []
            c["status"] = "Active" if c["is_active"] == 1 else "Inactive"

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
        group_ids = data.get("groupIds", [])

        is_active = 1 if data.get("status") == "Active" else 0

        db = get_db()
        cursor = db.cursor()

        # 1️⃣ Insert class
        cursor.execute("""
            INSERT INTO user_classes 
            (class_name, is_active, created_by)
            VALUES (%s, %s, %s)
        """, (
            data["className"],
            is_active,
            data.get("createdBy", "system")
        ))

        class_id = cursor.lastrowid

        # 2️⃣ Insert mapping records
        for group_id in group_ids:
            cursor.execute("""
                INSERT INTO user_class_groups (class_id, group_id)
                VALUES (%s, %s)
            """, (class_id, group_id))

        db.commit()
        db.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# UPDATE CLASS
# -----------------------------------
@user_classes_bp.put("/user-classes/<int:class_id>")
def update_class(class_id):
    try:
        data = request.json
        group_ids = data.get("groupIds", [])

        db = get_db()
        cursor = db.cursor()

        # 1️⃣ Check if class exists
        cursor.execute(
            "SELECT id FROM user_classes WHERE id = %s AND is_active = 1",
            (class_id,)
        )

        if cursor.fetchone() is None:
            db.close()
            return jsonify({"success": False, "message": "Class not found"}), 404

        # 2️⃣ Update class name
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

        # 3️⃣ Delete old group mappings
        cursor.execute("""
            DELETE FROM user_class_groups
            WHERE class_id = %s
        """, (class_id,))

        # 4️⃣ Insert new group mappings
        for group_id in group_ids:
            cursor.execute("""
                INSERT INTO user_class_groups (class_id, group_id)
                VALUES (%s, %s)
            """, (class_id, group_id))

        db.commit()
        db.close()

        return jsonify({
            "success": True,
            "message": "Class updated successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500



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
