# from flask import Blueprint, jsonify, request
# import mysql.connector
# import os
# import json
# from dotenv import load_dotenv

# load_dotenv()

# customfields_bp = Blueprint("customfields_bp", __name__)

# DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME"),
#     "port": int(os.getenv("DB_PORT", 3306))
# }

# def get_db():
#     return mysql.connector.connect(**DB_CONFIG)
# @customfields_bp.get("/customfields")
# def get_questions():
#     try:
#         db = get_db()
#         cursor = db.cursor(dictionary=True)

#         cursor.execute("""
#             SELECT id, question_text, question_type, answer_data, map_image
#             FROM customfields
#             WHERE is_active = 1
#             ORDER BY id DESC
#         """)

#         questions = cursor.fetchall()
#         db.close()

#         return jsonify({"success": True, "questions": questions})

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500
# @customfields_bp.get("/customfields/<int:question_id>")
# def get_question(question_id):
#     try:
#         db = get_db()
#         cursor = db.cursor(dictionary=True)

#         cursor.execute("""
#             SELECT * FROM customfields
#             WHERE id = %s AND is_active = 1
#         """, (question_id,))

#         question = cursor.fetchone()
#         db.close()

#         if not question:
#             return jsonify({"success": False, "message": "Question not found"}), 404

#         return jsonify({"success": True, "question": question})

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500
# @customfields_bp.post("/customfields")
# def add_question():
#     try:
#         data = request.json

#         if not data.get("questionText"):
#             return jsonify({"success": False, "message": "Question text is required"}), 400

#         answer_data = {
#             "options": data.get("options", []),
#             "correct": data.get("correctAnswer"),
#             "matchPairs": data.get("matchPairs", []),
#             "fillup_answer": data.get("correctAnswerText")
#         }

#         db = get_db()
#         cursor = db.cursor()

#         cursor.execute("""
#             INSERT INTO customfields
#             (question_text, question_type, answer_data, map_image, created_by)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (
#             data["questionText"],
#             data["questionType"],
#             json.dumps(answer_data),
#             data.get("mapImageBase64"),
#             "system"
#         ))

#         db.commit()
#         db.close()

#         return jsonify({"success": True, "message": "Question created successfully"})

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500
# @customfields_bp.put("/customfields/<int:question_id>")
# def update_question(question_id):
#     try:
#         data = request.json

#         db = get_db()
#         cursor = db.cursor()

#         cursor.execute("SELECT id FROM customfields WHERE id = %s", (question_id,))
#         if cursor.fetchone() is None:
#             return jsonify({"success": False, "message": "Question not found"}), 404

#         answer_data = {
#             "options": data.get("options", []),
#             "correct": data.get("correctAnswer"),
#             "matchPairs": data.get("matchPairs", []),
#             "fillup_answer": data.get("correctAnswerText")
#         }

#         cursor.execute("""
#             UPDATE customfields SET
#                 question_text = %s,
#                 question_type = %s,
#                 answer_data = %s,
#                 map_image = %s,
#                 updated_by = %s
#             WHERE id = %s
#         """, (
#             data["questionText"],
#             data["questionType"],
#             json.dumps(answer_data),
#             data.get("mapImageBase64"),
#             "system",
#             question_id
#         ))

#         db.commit()
#         db.close()

#         return jsonify({"success": True, "message": "Question updated successfully"})

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500
# @customfields_bp.delete("/customfields/<int:question_id>")
# def delete_question(question_id):
#     try:
#         db = get_db()
#         cursor = db.cursor()

#         cursor.execute("""
#             UPDATE customfields
#             SET is_active = 0
#             WHERE id = %s
#         """, (question_id,))

#         db.commit()
#         db.close()

#         return jsonify({"success": True, "message": "Question deleted successfully"})

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500
from flask import Blueprint, jsonify, request
import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

customfields_bp = Blueprint("customfields_bp", __name__)

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
# GET ALL QUESTIONS
# -----------------------------------
@customfields_bp.get("/customfields")
def get_questions():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, question_text, question_type, answer_data, map_image
            FROM customfields
            WHERE is_active = 1
            ORDER BY id DESC
        """)

        questions = cursor.fetchall()
        db.close()

        return jsonify({"success": True, "questions": questions})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------
# GET SINGLE QUESTION
# -----------------------------------
@customfields_bp.get("/customfields/<int:question_id>")
def get_question(question_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM customfields
            WHERE id = %s AND is_active = 1
        """, (question_id,))

        question = cursor.fetchone()
        db.close()

        if not question:
            return jsonify({"success": False, "message": "Question not found"}), 404

        return jsonify({"success": True, "question": question})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------
# CREATE QUESTION
# -----------------------------------
@customfields_bp.post("/customfields")
def add_question():
    try:
        data = request.json

        if not data.get("questionText"):
            return jsonify({"success": False, "message": "Question text is required"}), 400

        answer_data = {
            "options": data.get("options", []),
            "correct": data.get("correctAnswer"),
            "matchPairs": data.get("matchPairs", []),
            "fillup_answer": data.get("correctAnswerText")
        }

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO customfields
            (question_text, question_type, answer_data, map_image, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["questionText"],
            data["questionType"],
            json.dumps(answer_data),
            data.get("mapImageBase64"),
            "system"
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Question created successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------
# UPDATE QUESTION
# -----------------------------------
@customfields_bp.put("/customfields/<int:question_id>")
def update_question(question_id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM customfields WHERE id = %s", (question_id,))
        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "Question not found"}), 404

        answer_data = {
            "options": data.get("options", []),
            "correct": data.get("correctAnswer"),
            "matchPairs": data.get("matchPairs", []),
            "fillup_answer": data.get("correctAnswerText")
        }

        cursor.execute("""
            UPDATE customfields SET
                question_text = %s,
                question_type = %s,
                answer_data = %s,
                map_image = %s,
                updated_by = %s
            WHERE id = %s
        """, (
            data["questionText"],
            data["questionType"],
            json.dumps(answer_data),
            data.get("mapImageBase64"),
            "system",
            question_id
        ))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Question updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# -----------------------------------
# DELETE QUESTION (SOFT DELETE)
# -----------------------------------
@customfields_bp.delete("/customfields/<int:question_id>")
def delete_question(question_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE customfields
            SET is_active = 0
            WHERE id = %s
        """, (question_id,))

        db.commit()
        db.close()

        return jsonify({"success": True, "message": "Question deleted successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
