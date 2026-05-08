from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de données de recettes pour Smell'O
# Dosages en pourcentage (total 100%)
RECETTES = {
    "frais": {"pompe_1": 80, "pompe_2": 20},
    "sucre": {"pompe_1": 40, "pompe_2": 60},
    "boise": {"pompe_1": 10, "pompe_2": 90},
    "default": {"pompe_1": 50, "pompe_2": 50}
}

@app.route('/')
def home():
    return "<h1>Smell'O API</h1><p>Statut : Operationnelle</p>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupération du texte envoyé par l'ESP32
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Format JSON invalide"}), 400

        user_text = data.get("text", "").lower()
        
        # Logique d'analyse simplifiée
        selection = RECETTES["default"]
        for mot in RECETTES:
            if mot in user_text:
                selection = RECETTES[mot]
                break
        
        return jsonify({
            "status": "success",
            "recette": selection,
            "message": f"Analyse terminee pour : {user_text}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Indispensable pour Vercel
if __name__ == "__main__":
    app.run()
