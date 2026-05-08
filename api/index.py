from flask import Flask, jsonify, request

app = Flask(__name__)

# --- DICTIONNAIRE ENRICHI DES AMBIANCES (IA SIMULÉE) ---
# p1=Floral, p2=Oriental, p3=Rose, p4=Hespéridée, p5=Gourmand, p6=Fougère
AMBIANCES = {
    # SAISONS & NATURE
    "ete": {"p1": 20, "p2": 0, "p3": 10, "p4": 50, "p5": 10, "p6": 10, "msg": "Soleil éclatant : agrumes et fleurs légères."},
    "hiver": {"p1": 5, "p2": 45, "p3": 5, "p4": 0, "p5": 40, "p6": 5, "msg": "Coin du feu : épices chaudes et vanille réconfortante."},
    "printemps": {"p1": 60, "p2": 0, "p3": 20, "p4": 10, "p5": 0, "p6": 10, "msg": "Renouveau : bouquet de fleurs fraîches et rosée."},
    "automne": {"p1": 5, "p2": 25, "p3": 5, "p4": 5, "p5": 10, "p6": 50, "msg": "Feuilles mortes : terre humide et bois ambré."},
    "pluie": {"p1": 5, "p2": 5, "p3": 5, "p4": 25, "p5": 0, "p6": 60, "msg": "Pétrichor : l'odeur de la terre après l'orage."},
    "foret": {"p1": 10, "p2": 0, "p3": 5, "p4": 15, "p5": 0, "p6": 70, "msg": "Forêt profonde : mousse, herbe et bois sauvage."},
    "mer": {"p1": 10, "p2": 5, "p3": 5, "p4": 60, "p5": 5, "p6": 15, "msg": "Brise marine : notes iodées et zestes de citron."},
    "plage": {"p1": 15, "p2": 10, "p3": 5, "p4": 40, "p5": 20, "p6": 10, "msg": "Sable chaud : fleur de tiaré et noix de coco."},

    # MOMENTS DE LA JOURNÉE
    "matin": {"p1": 20, "p2": 0, "p3": 10, "p4": 60, "p5": 5, "p6": 5, "msg": "Réveil tonique : fraîcheur d'agrumes matinale."},
    "nuit": {"p1": 10, "p2": 50, "p3": 20, "p4": 0, "p5": 5, "p6": 15, "msg": "Mystère nocturne : oriental profond et envoûtant."},
    "soir": {"p1": 15, "p2": 30, "p3": 20, "p4": 10, "p5": 15, "p6": 10, "msg": "Coucher de soleil : douceur ambrée et rose."},

    # ÉMOTIONS & ÉTATS D'ESPRIT
    "zen": {"p1": 20, "p2": 20, "p3": 10, "p4": 10, "p5": 10, "p6": 30, "msg": "Méditation : équilibre parfait herbes et épices."},
    "energie": {"p1": 10, "p2": 5, "p3": 5, "p4": 75, "p5": 0, "p6": 5, "msg": "Boost : 100% vitalité hespéridée."},
    "romantique": {"p1": 20, "p2": 10, "p3": 60, "p4": 5, "p5": 5, "p6": 0, "msg": "Amour : la majesté de la rose rouge."},
    "douceur": {"p1": 15, "p2": 5, "p3": 10, "p4": 10, "p5": 55, "p6": 5, "msg": "Cocon : vanille et barbe à papa."},
    "fete": {"p1": 10, "p2": 10, "p3": 10, "p4": 20, "p5": 40, "p6": 10, "msg": "Cocktail : fruité, sucré et pétillant."},
    "sombre": {"p1": 0, "p2": 50, "p3": 10, "p4": 0, "p5": 0, "p6": 40, "msg": "Intense : cuir, fumée et bois mystique."},

    # LIEUX & VOYAGES
    "orient": {"p1": 5, "p2": 70, "p3": 20, "p4": 0, "p5": 5, "p6": 0, "msg": "Palais arabe : ambre précieux et musc."},
    "bibliotheque": {"p1": 5, "p2": 40, "p3": 5, "p4": 5, "p5": 5, "p6": 40, "msg": "Vieux livres : papier jauni et bois ciré."},
    "jardin": {"p1": 70, "p2": 0, "p3": 15, "p4": 5, "p5": 0, "p6": 10, "msg": "Parterre fleuri : explosion de pétales."},
    "maroc": {"p1": 10, "p2": 40, "p3": 20, "p4": 20, "p5": 5, "p6": 5, "msg": "Médina : fleurs d'oranger et épices du souk."},
    "provence": {"p1": 40, "p2": 0, "p3": 10, "p4": 10, "p5": 0, "p6": 40, "msg": "Sud : lavande et herbes de Provence."},
    "paris": {"p1": 30, "p2": 20, "p3": 30, "p4": 10, "p5": 10, "p6": 0, "msg": "Chic : poudré, floral et élégant."}
}

@app.route('/')
def home():
    return "<h1>Smell'O IA Active</h1></p>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data: return jsonify({"status": "error", "message": "JSON manquant"}), 400
        
        user_input = data.get("text", "").lower()
        
        # Valeurs par défaut si aucun mot-clé n'est trouvé
        res_recette = {"p1":16,"p2":16,"p3":17,"p4":17,"p5":17,"p6":17}
        ambiance_nom = "Signature"
        msg = "Mélange spécial Smell'O."

        # Recherche intelligente par mot-clé
        for cle, valeur in AMBIANCES.items():
            if cle in user_input:
                temp_valeur = valeur.copy()
                msg = temp_valeur.pop("msg")
                res_recette = temp_valeur
                ambiance_nom = cle.capitalize()
                break
        
        return jsonify({
            "status": "success",
            "ambiance": ambiance_nom,
            "recette": res_recette,
            "message": msg
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
