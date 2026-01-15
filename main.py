from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running"

@app.route("/estimation", methods=["POST"])
def estimate():
    data = request.get_json()
    adresse = data.get("adresse")
    chambres = data.get("chambres")

    if not adresse or not chambres:
        return jsonify({"error": "Adresse ou chambres manquants"}), 400

    try:
        # Setup Chrome en headless (sans interface graphique)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)

        # Aller sur la page du simulateur
        driver.get("https://hello.pricelabs.co/fr/calculer-votre-estimation-de-revenus/")

        wait = WebDriverWait(driver, 15)

        # Remplir l’adresse
        champ_adresse = wait.until(EC.presence_of_element_located((By.ID, "address")))
        champ_adresse.clear()
        champ_adresse.send_keys(adresse)
        time.sleep(2)

        # Choisir la devise (EUR)
        select_devise = wait.until(EC.presence_of_element_located((By.ID, "currency")))
        select_devise.send_keys("EUR")

        # Nombre de chambres
        select_chambres = wait.until(EC.presence_of_element_located((By.ID, "bedrooms")))
        select_chambres.send_keys(str(chambres))
        time.sleep(1)

        # Attendre que les résultats apparaissent
        revenu_annuel_el = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Revenus annuels')]/following-sibling::div")))
        revenu_annuel = revenu_annuel_el.text

        revenu_mensuel = str(int(int(revenu_annuel.replace("€", "").replace(",", "").replace("/mo", "").strip()) / 12))

        # Percentiles et autres
        p25 = driver.find_element(By.XPATH, "//div[contains(text(),'25e percentile')]/following-sibling::div").text
        p50 = driver.find_element(By.XPATH, "//div[contains(text(),'50e percentile')]/following-sibling::div").text
        p75 = driver.find_element(By.XPATH, "//div[contains(text(),'75e percentile')]/following-sibling::div").text
        occupation = driver.find_element(By.XPATH, "//div[contains(text(),'Occupation moyenne')]/following-sibling::div").text

        driver.quit()

        return jsonify({
            "revenu_annuel": revenu_annuel,
            "revenu_mensuel": revenu_mensuel,
            "percentile_25": p25,
            "percentile_50": p50,
            "percentile_75": p75,
            "occupation": occupation
        })

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route('/', methods=['POST'])
def estimation():
    print("➡️ Requête reçue")
    data = request.json
    print("📦 Données reçues:", data)

    try:
        # Ton scraping ici...
        result = scrap_pricelabs(data['adresse'], data['chambres'])
        print("✅ Résultat:", result)
        return jsonify(result)
    except Exception as e:
        print("❌ Erreur serveur:", e)
        return jsonify({"error": str(e)}), 500

