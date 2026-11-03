
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/students", methods=["GET"])
def get_students():
    conn = connect_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = connect_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data or not all(data.get(k) for k in ["name", "department", "email"]):
        return jsonify({"error": "Name, department and email are required"}), 400

    conn = connect_db()
    cursor = conn.execute(
        "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
        (data["name"], data["department"], data["email"])
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added successfully",
        "id": student_id
    }), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)

    if not data or not all(data.get(k) for k in ["name", "department", "email"]):
        return jsonify({"error": "Name, department and email are required"}), 400

    conn = connect_db()
    cursor = conn.execute(
        """UPDATE students
           SET name = ?, department = ?, email = ?
           WHERE id = ?""",
        (data["name"], data["department"], data["email"], student_id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?", (student_id,)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5000)
