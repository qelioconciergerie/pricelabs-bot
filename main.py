from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def estimation():
    data = request.get_json()
    adresse = data.get("adresse")
    chambres = data.get("chambres")

    if not adresse or not chambres:
        return jsonify({"error": "Champs manquants"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Aller sur la page de simulation
            page.goto("https://hello.pricelabs.co/fr/calculer-votre-estimation-de-revenus/")
            
            # Remplir le formulaire
            page.fill("input[placeholder='Ex: 10 rue du Louvre Paris']", adresse)
            page.select_option("select[name='bedrooms']", str(chambres))
            page.click("text=Calculer mes revenus")

            # Attendre que les résultats soient visibles (adapter les sélecteurs si besoin)
            page.wait_for_selector("text=Revenu mensuel estimé", timeout=15000)

            # Récupérer les résultats
            revenu_mensuel = page.locator(".results-card span.font-bold").nth(0).text_content()
            revenu_annuel = page.locator(".results-card span.font-bold").nth(1).text_content()
            percentile_25 = page.locator(".results-card span.font-bold").nth(2).text_content()
            percentile_50 = page.locator(".results-card span.font-bold").nth(3).text_content()
            percentile_75 = page.locator(".results-card span.font-bold").nth(4).text_content()
            occupation = page.locator(".results-card span.font-bold").nth(5).text_content()

            browser.close()

        return jsonify({
            "revenu_mensuel": revenu_mensuel,
            "revenu_annuel": revenu_annuel,
            "percentile_25": percentile_25,
            "percentile_50": percentile_50,
            "percentile_75": percentile_75,
            "occupation": occupation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
