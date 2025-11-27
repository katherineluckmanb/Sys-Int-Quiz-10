# main.py
# from urllib import request
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, get_jwt
import datetime

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "your-very-secure-jwt-signing-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
jwt = JWTManager(app)

# Mock database of users with their roles (for Authorization)
USERS = {
    "alice": {"password": "password123", "roles": ["user"]},
    "bob": {"password": "password456", "roles": ["admin", "user"]},
}


@app.route("/")
def root():
    """
    Root endpoint to check API health.
    """
    return jsonify({"status": "ok", "version": "1.0.0"})

@app.route("/login", methods=["POST"])
def login():
    """
    User login to generate JWT token.
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username not in USERS or USERS[username]["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401
    additional_claims = {"roles": USERS[username]["roles"]} 
    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    """
    Simple logic function to test mathematics.
    """
    return jsonify({"result": a + b})


@app.route("/substract/<int:a>/<int:b>", methods=["GET"])
@jwt_required()
def substract(a, b):
    """
    Simple logic function to test mathematics.
    """
    return jsonify({"result": a - b})   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

