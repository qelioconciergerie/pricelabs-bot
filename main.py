from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route("/estimation", methods=["POST"])
def estimation():
    try:
        data = request.json
        adresse = data.get("adresse")
        auteur = data.get("auteur")
        chambres = data.get("chambres")

        if not adresse or not auteur or not chambres:
            return jsonify({"error": "Champs manquants"}), 400

        # Configuration de Selenium avec Chrome Headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.pricelabs.co/market-dashboard/estimator")

        wait = WebDriverWait(driver, 15)

        # Adresse
        adresse_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='adresse']")))
        adresse_input.clear()
        adresse_input.send_keys(adresse)
        time.sleep(2)

        # Devise
        currency_select = driver.find_element(By.CSS_SELECTOR, "select[name='currency']")
        currency_select.send_keys("EUR")

        # Nombre de chambres
        chambre_select = driver.find_element(By.CSS_SELECTOR, "select[name='bedrooms']")
        chambre_select.send_keys(str(chambres))

        # Bouton d'estimation
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

        time.sleep(5)

        # Récupération des résultats
        revenu_mensuel = driver.find_element(By.XPATH, "//h2[contains(text(), '€/mo')]").text.replace("€/mo", "").strip()
        revenu_annuel = driver.find_element(By.XPATH, "//div[contains(text(),'Revenus de')]").text.split("€")[-1].strip()

        percentile_25 = driver.find_element(By.XPATH, "//div[contains(text(),'25e percentile')]/following-sibling::div").text.replace("€", "").strip()
        percentile_50 = driver.find_element(By.XPATH, "//div[contains(text(),'50e percentile')]/following-sibling::div").text.replace("€", "").strip()
        percentile_75 = driver.find_element(By.XPATH, "//div[contains(text(),'75e percentile')]/following-sibling::div").text.replace("€", "").strip()
        occupation = driver.find_element(By.XPATH, "//div[contains(text(),'Occupation moyenne')]/following-sibling::div").text.replace("%", "").strip()

        driver.quit()

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
