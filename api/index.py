from flask import Flask, jsonify, request

app = Flask(__name__)

# CONFIGURATION SMELL'O - 6 FAMILLES OLFACTIVES
# p1 = Floral (Fleurs légères)
# p2 = Oriental (Épices, ambre)
# p3 = Rose (Note de cœur puissante)
# p4 = Hespéridée (Agrumes, frais)
# p5 = Gourmand (Vanille, chocolat, caramel)
# p6 = Fougère (Lavande, mousse, herbe)

RECETTES = {
    "romantique": {
        "p1": 50, "p2": 5, "p3": 30, "p4": 5, "p5": 5, "p6": 5,
        "desc": "Un mélange doux dominé par les fleurs et la rose."
    },
    "mysterieux": {
        "p1": 5, "p2": 60, "p3": 10, "p4": 5, "p5": 10, "p6": 10,
        "desc": "Oriental intense avec une touche gourmande et boisée."
    },
    "frais": {
        "p1": 15, "p2": 5, "p3": 5, "p4": 60, "p5": 5, "p6": 10,
        "desc": "Explosion d'agrumes (Hespéridée) pour un réveil énergique."
    },
    "douceur": {
        "p1": 10, "p2": 10, "p3": 10, "p4": 5, "p5": 60, "p6": 5,
        "desc": "Parfum Gourmand rappelant la vanille et les pâtisseries."
    },
    "nature": {
        "p1": 10, "p2": 5, "p3": 5, "p4": 15, "p5": 5, "p6": 60,
        "desc": "L'odeur de la forêt et de la lavande (Fougère)."
    },
    "orient": {
        "p1": 10, "p2": 50, "p3": 20, "p4": 5, "p5": 10, "p6": 5,
        "desc": "Un voyage chaud mêlant épices orientales et rose royale."
    },
    "ete": {
        "p1": 25, "p2": 5, "p3": 10, "p4": 40, "p5": 10, "p6": 10,
        "desc": "Mélange léger de fleurs et d'agrumes."
    },
    "default": {
        "p1": 16, "p2": 16, "p3": 17, "p4": 17, "p5": 17, "p6": 17,
        "desc": "Mélange équilibré de toutes les fragrances."
    }
}

@app.route('/')
def home():
    return "<h1>Smell'O API v3</h1><p>Configuration 6 Pompes : ACTIVE</p>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "JSON invalide"}), 400

        user_text = data.get("text", "").lower()
        
        selection = RECETTES["default"]
        match_nom = "Melange Signature"

        # Logique de détection par mots-clés
        if "frais" in user_text or "citron" in user_text:
            selection = RECETTES["frais"]
            match_nom = "Frais & Hespéridé"
        elif "rose" in user_text or "amour" in user_text:
            selection = RECETTES["romantique"]
            match_nom = "Romantique"
        elif "sucre" in user_text or "bonbon" in user_text or "vanille" in user_text:
            selection = RECETTES["douceur"]
            match_nom = "Gourmand"
        elif "epice" in user_text or "nuit" in user_text:
            selection = RECETTES["mysterieux"]
            match_nom = "Oriental Mystérieux"
        elif "foret" in user_text or "herbe" in user_text:
            selection = RECETTES["nature"]
            match_nom = "Fougère Sauvage"

        return jsonify({
            "status": "success",
            "nom_parfum": match_nom,
            "recette": selection,
            "message": selection["desc"]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
