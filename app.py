from flask import Flask, jsonify, request
import engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/login", methods=["GET"])
def login():
    return jsonify({"message": "Login endpoint"})

@app.route("/get_data", methods=["POST"])
def Lead_Generator():
    data = request.json.get("value")
    
    result = engine.Engine(data)
    
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()
