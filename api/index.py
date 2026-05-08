from flask import Flask, jsonify, request
from supabase import create_client, Client

app = Flask(__name__)

# --- CONFIGURATION SUPABASE ---
# Ton URL de projet et ta clé ANON (Public)
SUPABASE_URL = "https://bemtohsqjieqnenmjeee.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlbXRvaHNxamllcW5lbm1qZWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyMjE3NTEsImV4cCI6MjA5Mzc5Nzc1MX0.ROGbHuZM3j05Kv-G64qQcH1gtJpJNntWeE92nxPOp10"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- DICTIONNAIRE DES 20 AMBIANCES ---
# p1=Floral, p2=Oriental, p3=Rose, p4=Hespéridée, p5=Gourmand, p6=Fougère
AMBIANCES = {
    "ete": {"p1": 20, "p2": 0, "p3": 10, "p4": 50, "p5": 10, "p6": 10, "msg": "Soleil éclatant : agrumes et fleurs légères."},
    "hiver": {"p1": 5, "p2": 45, "p3": 5, "p4": 0, "p5": 40, "p6": 5, "msg": "Coin du feu : épices chaudes et vanille réconfortante."},
    "printemps": {"p1": 60, "p2": 0, "p3": 20, "p4": 10, "p5": 0, "p6": 10, "msg": "Renouveau : un bouquet de fleurs fraîches et de rose."},
    "automne": {"p1": 5, "p2": 25, "p3": 5, "p4": 5, "p5": 10, "p6": 50, "msg": "Feuilles mortes : terre humide et bois ambré."},
    "pluie": {"p1": 5, "p2": 5, "p3": 5, "p4": 25, "p5": 0, "p6": 60, "msg": "Pétrichor : l'odeur de la terre après l'orage."},
    "matin": {"p1": 20, "p2": 0, "p3": 10, "p4": 60, "p5": 5, "p6": 5, "msg": "Réveil tonique : fraîcheur d'agrumes et rosée du matin."},
    "midi": {"p1": 30, "p2": 5, "p3": 20, "p4": 30, "p5": 5, "p6": 10, "msg": "Plein soleil : un mélange floral et pétillant."},
    "soir": {"p1": 15, "p2": 30, "p3": 20, "p4": 10, "p5": 15, "p6": 10, "msg": "Coucher de soleil : douceur ambrée et rose élégante."},
    "nuit": {"p1": 10, "p2": 50, "p3": 20, "p4": 0, "p5": 5, "p6": 15, "msg": "Mystère nocturne : oriental profond et envoûtant."},
    "nature": {"p1": 10, "p2": 0, "p3": 5, "p4": 15, "p5": 0, "p6": 70, "msg": "Forêt profonde : mousse, herbe et bois sauvage."},
    "orient": {"p1": 5, "p2": 70, "p3": 20, "p4": 0, "p5": 5, "p6": 0, "msg": "Souk de nuit : épices rares et rose précieuse."},
    "plage": {"p1": 15, "p2": 10, "p3": 5, "p4": 40, "p5": 20, "p6": 10, "msg": "Sable chaud : agrumes mêlés à une note coco-gourmande."},
    "jardin": {"p1": 70, "p2": 0, "p3": 15, "p4": 5, "p5": 0, "p6": 10, "msg": "Parterre fleuri : explosion de pétales et de pollen."},
    "zen": {"p1": 20, "p2": 20, "p3": 10, "p4": 10, "p5": 10, "p6": 30, "msg": "Méditation : équilibre parfait entre herbes et épices."},
    "energie": {"p1": 10, "p2": 5, "p3": 5, "p4": 75, "p5": 0, "p6": 5, "msg": "Boost : 100% vitalité hespéridée."},
    "romantique": {"p1": 20, "p2": 10, "p3": 60, "p4": 5, "p5": 5, "p6": 0, "msg": "Dîner aux chandelles : la majesté de la rose."},
    "fete": {"p1": 10, "p2": 10, "p3": 10, "p4": 20, "p5": 40, "p6": 10, "msg": "Célébration : cocktail gourmand et pétillant."},
    "sombre": {"p1": 0, "p2": 50, "p3": 10, "p4": 0, "p5": 0, "p6": 40, "msg": "Gothique : bois sombre et orient mystique."},
    "douceur": {"p1": 15, "p2": 5, "p3": 10, "p4": 10, "p5": 55, "p6": 5, "msg": "Cocon : vanille et gourmandises d'enfance."},
    "bibliotheque": {"p1": 5, "p2": 40, "p3": 5, "p4": 5, "p5": 5, "p6": 40, "msg": "Vieux livres : cuir et bois poudré."}
}

@app.route('/')
def home():
    return "<h1>Smell'O API - Statut OK</h1><p>Connectee a Supabase : bemtohsqjieqnenmjeee</p>"

# ROUTE POUR L'IA (PREDICTION)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "No JSON provided"}), 400
        
        user_input = data.get("text", "").lower()
        
        # Recette par défaut
        res_recette = {"p1":16,"p2":16,"p3":17,"p4":17,"p5":17,"p6":17}
        ambiance_nom = "Signature"
        message = "Votre parfum sur mesure par Smell'O."

        # Recherche du mot clé dans les 20 ambiances
        for cle, valeur in AMBIANCES.items():
            if cle in user_input:
                res_recette = valeur.copy()
                ambiance_nom = cle.capitalize()
                message = res_recette.pop("msg") # On enlève 'msg' pour ne laisser que les pompes
                break
        
        return jsonify({
            "status": "success",
            "ambiance": ambiance_nom,
            "recette": res_recette,
            "message": message
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ROUTE POUR LES FAVORIS (SUPABASE)
@app.route('/save-favorite', methods=['POST'])
def save_favorite():
    try:
        data = request.get_json()
        nom = data.get("nom_parfum")
        recette = data.get("recette")

        if not nom or not recette:
            return jsonify({"error": "Donnees manquantes (nom ou recette)"}), 400

        # Insertion dans la table 'favoris'
        response = supabase.table("favoris").insert({
            "nom_parfum": nom, 
            "recette": recette
        }).execute()
        
        return jsonify({
            "status": "success", 
            "message": f"Le parfum '{nom}' est enregistre !",
            "data": response.data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
