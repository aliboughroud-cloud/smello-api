from flask import Flask, jsonify, request

app = Flask(__name__)

# p1=Floral, p2=Oriental, p3=Rose, p4=Hespéridée (Citrus), p5=Gourmand, p6=Fougère
AMBIANCES = {
    # --- SAISONS & TEMPS ---
    "ete": {"p1": 20, "p2": 0, "p3": 10, "p4": 50, "p5": 10, "p6": 10, "msg": "Soleil éclatant : agrumes et fleurs légères."},
    "hiver": {"p1": 5, "p2": 45, "p3": 5, "p4": 0, "p5": 40, "p6": 5, "msg": "Coin du feu : épices chaudes et vanille réconfortante."},
    "printemps": {"p1": 60, "p2": 0, "p3": 20, "p4": 10, "p5": 0, "p6": 10, "msg": "Renouveau : un bouquet de fleurs fraîches et de rose."},
    "automne": {"p1": 5, "p2": 25, "p3": 5, "p4": 5, "p5": 10, "p6": 50, "msg": "Feuilles mortes : terre humide et bois ambré."},
    "pluie": {"p1": 5, "p2": 5, "p3": 5, "p4": 25, "p5": 0, "p6": 60, "msg": "Pétrichor : l'odeur de la terre après l'orage."},

    # --- MOMENTS DE LA JOURNÉE ---
    "matin": {"p1": 20, "p2": 0, "p3": 10, "p4": 60, "p5": 5, "p6": 5, "msg": "Réveil tonique : fraîcheur d'agrumes et rosée du matin."},
    "midi": {"p1": 30, "p2": 5, "p3": 20, "p4": 30, "p5": 5, "p6": 10, "msg": "Plein soleil : un mélange floral et pétillant."},
    "soir": {"p1": 15, "p2": 30, "p3": 20, "p4": 10, "p5": 15, "p6": 10, "msg": "Coucher de soleil : douceur ambrée et rose élégante."},
    "nuit": {"p1": 10, "p2": 50, "p3": 20, "p4": 0, "p5": 5, "p6": 15, "msg": "Mystère nocturne : oriental profond et envoûtant."},

    # --- LIEUX & VOYAGES ---
    "nature": {"p1": 10, "p2": 0, "p3": 5, "p4": 15, "p5": 0, "p6": 70, "msg": "Forêt profonde : mousse, herbe et bois sauvage."},
    "orient": {"p1": 5, "p2": 70, "p3": 20, "p4": 0, "p5": 5, "p6": 0, "msg": "Souk de nuit : épices rares et rose précieuse."},
    "plage": {"p1": 15, "p2": 10, "p3": 5, "p4": 40, "p5": 20, "p6": 10, "msg": "Sable chaud : agrumes mêlés à une note coco-gourmande."},
    "jardin": {"p1": 70, "p2": 0, "p3": 15, "p4": 5, "p5": 0, "p6": 10, "msg": "Parterre fleuri : explosion de pétales et de pollen."},

    # --- ÉMOTIONS & ÉTATS D'ESPRIT ---
    "zen": {"p1": 20, "p2": 20, "p3": 10, "p4": 10, "p5": 10, "p6": 30, "msg": "Méditation : équilibre parfait entre herbes et épices."},
    "energie": {"p1": 10, "p2": 5, "p3": 5, "p4": 75, "p5": 0, "p6": 5, "msg": "Boost : 100% vitalité hespéridée."},
    "romantique": {"p1": 20, "p2": 10, "p3": 60, "p4": 5, "p5": 5, "p6": 0, "msg": "Dîner aux chandelles : la majesté de la rose."},
    "fete": {"p1": 10, "p2": 10, "p3": 10, "p4": 20, "p5": 40, "p6": 10, "msg": "Célébration : cocktail gourmand et pétillant."},

    # --- AMBIANCES "CONCEPT" ---
    "sombre": {"p1": 0, "p2": 50, "p3": 10, "p4": 0, "p5": 0, "p6": 40, "msg": "Gothique : bois sombre et orient mystique."},
    "douceur": {"p1": 15, "p2": 5, "p3": 10, "p4": 10, "p5": 55, "p6": 5, "msg": "Cocon : vanille et gourmandises d'enfance."},
    "bibliotheque": {"p1": 5, "p2": 40, "p3": 5, "p4": 5, "p5": 5, "p6": 40, "msg": "Vieux livres : mélange de papier (fougère) et de cuir (oriental)."}
}

@app.route('/')
def home():
    return f"<h1>Smell'O - Intelligence Olfactive</h1><p>{len(AMBIANCES)} Ambiances configurees.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        user_input = data.get("text", "").lower()
        
        # Par défaut : Ambiance Signature
        res = {"recette": {"p1":16,"p2":16,"p3":17,"p4":17,"p5":17,"p6":17}, "ambiance": "Signature", "msg": "Votre parfum sur mesure."}

        # On parcourt les 20 ambiances pour trouver un match
        for cle, valeur in AMBIANCES.items():
            if cle in user_input:
                res["recette"] = valeur
                res["ambiance"] = cle.capitalize()
                res["msg"] = valeur["msg"]
                break
        
        # Nettoyage pour ne pas renvoyer le "msg" dans la recette elle-même
        if "msg" in res["recette"]:
            del res["recette"]["msg"]

        return jsonify(res)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
