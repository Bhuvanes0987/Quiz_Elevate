from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

customfieldgroups_bp = Blueprint("customfieldgroups_bp", __name__)

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
# GET ALL CUSTOM FIELD GROUPS
# -----------------------------------
@customfieldgroups_bp.get("/custom-field-groups")
def get_groups():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, group_name
            FROM custom_field_groups
            WHERE is_active = 1
            ORDER BY id DESC
        """)
        groups = cursor.fetchall()

        for group in groups:
            cursor.execute("""
                SELECT id, field_name AS name
                FROM custom_fields
                WHERE group_id = %s
            """, (group["id"],))
            group["fields"] = cursor.fetchall()
            group["questionText"] = group.pop("group_name")

        db.close()
        return jsonify({"success": True, "groups": groups})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# GET SINGLE GROUP
# -----------------------------------
@customfieldgroups_bp.get("/custom-field-groups/<int:group_id>")
def get_group(group_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, group_name
            FROM custom_field_groups
            WHERE id = %s AND is_active = 1
        """, (group_id,))
        group = cursor.fetchone()

        if not group:
            return jsonify({"success": False, "message": "Group not found"}), 404

        cursor.execute("""
            SELECT id, field_name AS name
            FROM custom_fields
            WHERE group_id = %s
        """, (group_id,))
        fields = cursor.fetchall()

        db.close()

        return jsonify({
            "success": True,
            "group": {
                "id": group["id"],
                "questionText": group["group_name"],
                "fields": fields
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# CREATE GROUP
# -----------------------------------
@customfieldgroups_bp.post("/custom-field-groups")
def create_group():
    try:
        data = request.json
        print("🔥 Incoming POST data:", data)

        if not data.get("questionText"):
            return jsonify({"success": False, "message": "Group name is required"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO custom_field_groups (group_name, created_by)
            VALUES (%s, %s)
        """, (data["questionText"], "system"))

        group_id = cursor.lastrowid

        for field in data.get("fields", []):
            cursor.execute("""
                INSERT INTO custom_fields (group_id, field_name)
                VALUES (%s, %s)
            """, (group_id, field["name"]))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Group created successfully"})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# UPDATE GROUP
# -----------------------------------
@customfieldgroups_bp.put("/custom-field-groups/<int:group_id>")
def update_group(group_id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id FROM custom_field_groups
            WHERE id = %s AND is_active = 1
        """, (group_id,))
        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "Group not found"}), 404

        cursor.execute("""
            UPDATE custom_field_groups
            SET group_name = %s, updated_by = %s
            WHERE id = %s
        """, (data["questionText"], "system", group_id))

        cursor.execute("""
            DELETE FROM custom_fields
            WHERE group_id = %s
        """, (group_id,))

        for field in data.get("fields", []):
            cursor.execute("""
                INSERT INTO custom_fields (group_id, field_name)
                VALUES (%s, %s)
            """, (group_id, field["name"]))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Group updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# -----------------------------------
# DELETE GROUP (SOFT DELETE)
# -----------------------------------
@customfieldgroups_bp.delete("/custom-field-groups/<int:group_id>")
def delete_group(group_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE custom_field_groups
            SET is_active = 0
            WHERE id = %s
        """, (group_id,))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Group deleted successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
    
@customfieldgroups_bp.post("/custom-field-groups")
def add_group():
    data = request.json
    print("🔥 Incoming POST data:", data)

    try:
        db = get_db()
        cursor = db.cursor()

        # Insert into customfields table
        cursor.execute("""
            INSERT INTO customfields
            (question_text, question_type, answer_data, created_by)
            VALUES (%s, %s, %s, %s)
        """, (
            data["questionText"],
            "custom_group",   # mark type as group
            json.dumps({"fields": data.get("fields", [])}),
            "system"
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Group created successfully"})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500
