from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "API Smell'O opérationnelle !"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get("text", "")
    # Simulation de dosage pour l'instant
    return jsonify({"pompe_1": 50, "pompe_2": 50})

if __name__ == "__main__":
    app.run()