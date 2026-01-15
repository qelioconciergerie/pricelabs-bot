from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def estimation():
    data = request.get_json()

    # Vérification des champs requis
    required_fields = ["adresse", "auteur", "chambres"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Champs manquants"}), 400

    adresse = data["adresse"]
    auteur = data["auteur"]
    chambres = data["chambres"]

    # Simuler un calcul d'estimation
    estimation = {
        "revenus_mensuel": 1000 + 100 * int(chambres),
        "revenus_annuel": (1000 + 100 * int(chambres)) * 12,
        "percentile_25": 900,
        "percentile_50": 1100,
        "percentile_75": 1300,
        "occupation": "80%"
    }

    return jsonify({
        "adresse": adresse,
        "auteur": auteur,
        "chambres": chambres,
        "estimation": estimation
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
