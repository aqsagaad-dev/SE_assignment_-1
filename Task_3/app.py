
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

users = {
    "employee": {
        "password": "emp123",
        "role": "Employee"
    },
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    }
}

tokens = {}

employees = [
    {"id": 1, "name": "Ayesha Khan", "department": "HR"},
    {"id": 2, "name": "Hira Ahmed", "department": "IT"},
    {"id": 3, "name": "Maham Ali", "department": "Finance"},
    {"id": 4, "name": "Zoya Memon", "department": "Marketing"}
]


def authenticate(required_role=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            token = request.headers.get("Authorization")

            if not token or token not in tokens:
                return jsonify({
                    "error": "Unauthorized. Please login first."
                }), 401

            username = tokens[token]
            role = users[username]["role"]

            if required_role == "Administrator" and role != "Administrator":
                return jsonify({
                    "error": "Forbidden. Admin access required."
                }), 403

            return function(*args, **kwargs)

        return wrapper
    return decorator


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON data not received"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password required"
        }), 400

    if username not in users or users[username]["password"] != password:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    token = username + "_token"
    tokens[token] = username

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": users[username]["role"],
        "token": token
    }), 200


@app.route("/employees", methods=["GET"])
@authenticate()
def get_employees():
    return jsonify(employees), 200


@app.route("/employees", methods=["POST"])
@authenticate("Administrator")
def add_employee():

    data = request.get_json(silent=True)

    if not data or not data.get("name") or not data.get("department"):
        return jsonify({
            "error": "Name and department are required"
        }), 400

    new_id = max([employee["id"] for employee in employees], default=0) + 1

    new_employee = {
        "id": new_id,
        "name": data["name"],
        "department": data["department"]
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201


@app.route("/employees/<int:employee_id>", methods=["PUT"])
@authenticate("Administrator")
def update_employee(employee_id):

    data = request.get_json(silent=True)

    if not data or not data.get("name") or not data.get("department"):
        return jsonify({
            "error": "Name and department are required"
        }), 400

    for employee in employees:
        if employee["id"] == employee_id:

            employee["name"] = data["name"]
            employee["department"] = data["department"]

            return jsonify({
                "message": "Employee updated successfully"
            }), 200

    return jsonify({
        "error": "Employee not found"
    }), 404


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
@authenticate("Administrator")
def delete_employee(employee_id):

    for employee in employees:
        if employee["id"] == employee_id:

            employees.remove(employee)

            return jsonify({
                "message": "Employee deleted successfully"
            }), 200

    return jsonify({
        "error": "Employee not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True, port=5002)
