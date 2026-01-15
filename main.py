from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def estimation():
    data = request.get_json()

    adresse = data.get("adresse")
    chambres = data.get("chambres")

    if not adresse or not chambres:
        return jsonify({"error": "Champs manquants"}), 400

    estimation_result = {
        "revenu_mensuel": 2000,
        "revenu_annuel": 24000,
        "percentile_25": 1800,
        "percentile_50": 2000,
        "percentile_75": 2200,
        "occupation": "85%"
    }

    return jsonify(estimation_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
