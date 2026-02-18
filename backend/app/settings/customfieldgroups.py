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
# GET ALL CUSTOM FIELD GROUPS (FIXED)
# -----------------------------------
@customfieldgroups_bp.get("/custom-field-groups")
def get_groups():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT 
            g.id,
            g.group_name,
            GROUP_CONCAT(DISTINCT c.class_name SEPARATOR ', ') AS classNames,
            GROUP_CONCAT(DISTINCT c.id) AS classIds
        FROM custom_field_groups g
        LEFT JOIN user_class_groups ucg ON ucg.group_id = g.id
        LEFT JOIN user_classes c ON c.id = ucg.class_id
        WHERE g.is_active = 1
        GROUP BY g.id
        ORDER BY g.id DESC
        """

        cursor.execute(query)
        groups = cursor.fetchall()

        for group in groups:

            # Fetch fields
            cursor.execute("""
                SELECT id, field_name AS name
                FROM custom_fields
                WHERE group_id = %s
            """, (group["id"],))
            group["fields"] = cursor.fetchall()

            group["questionText"] = group.pop("group_name")

            # Convert classIds string → array
            if group["classIds"]:
                group["classIds"] = [
                    int(x) for x in group["classIds"].split(",")
                ]
            else:
                group["classIds"] = []

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

        # Fetch fields
        cursor.execute("""
            SELECT id, field_name AS name
            FROM custom_fields
            WHERE group_id = %s
        """, (group_id,))
        fields = cursor.fetchall()

        # Fetch mapped class IDs
        cursor.execute("""
            SELECT class_id
            FROM user_class_groups
            WHERE group_id = %s
        """, (group_id,))
        class_rows = cursor.fetchall()
        class_ids = [row["class_id"] for row in class_rows]

        db.close()

        return jsonify({
            "success": True,
            "group": {
                "id": group["id"],
                "questionText": group["group_name"],
                "fields": fields,
                "classIds": class_ids
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

        if not data.get("questionText"):
            return jsonify({"success": False, "message": "Group name is required"}), 400

        db = get_db()
        cursor = db.cursor()

        # Insert group
        cursor.execute("""
            INSERT INTO custom_field_groups (group_name, created_by, is_active)
            VALUES (%s, %s, 1)
        """, (data["questionText"], "system"))

        group_id = cursor.lastrowid

        # Insert fields
        for field in data.get("fields", []):
            cursor.execute("""
                INSERT INTO custom_fields (group_id, field_name)
                VALUES (%s, %s)
            """, (group_id, field["name"]))

        # Insert class mappings
        for class_id in data.get("classIds", []):
            cursor.execute("""
                INSERT INTO user_class_groups (class_id, group_id)
                VALUES (%s, %s)
            """, (class_id, group_id))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Group created successfully"})

    except Exception as e:
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

        # Update group name
        cursor.execute("""
            UPDATE custom_field_groups
            SET group_name = %s, updated_by = %s
            WHERE id = %s
        """, (data["questionText"], "system", group_id))

        # Delete old fields
        cursor.execute("DELETE FROM custom_fields WHERE group_id = %s", (group_id,))

        # Insert new fields
        for field in data.get("fields", []):
            cursor.execute("""
                INSERT INTO custom_fields (group_id, field_name)
                VALUES (%s, %s)
            """, (group_id, field["name"]))

        # Delete old mappings
        cursor.execute("DELETE FROM user_class_groups WHERE group_id = %s", (group_id,))

        # Insert new mappings
        for class_id in data.get("classIds", []):
            cursor.execute("""
                INSERT INTO user_class_groups (class_id, group_id)
                VALUES (%s, %s)
            """, (class_id, group_id))

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
