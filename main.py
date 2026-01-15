from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/estimation', methods=['POST'])
def estimation():
    try:
        # 1. Récupération des données reçues
        data = request.get_json()
        adresse = data.get("adresse")
        chambres = str(data.get("chambres"))

        # 2. Préparation de Selenium avec Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)

        # 3. Aller sur PriceLabs
        driver.get("https://hello.pricelabs.co/fr/calculer-votre-estimation-de-revenus/")
        wait = WebDriverWait(driver, 20)

        # 4. Remplir les champs
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="adresse"]')))
        input_adresse = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="adresse"]')
        input_adresse.clear()
        input_adresse.send_keys(adresse)

        select_chambres = driver.find_element(By.CSS_SELECTOR, 'select[name="bedrooms"]')
        select_chambres.send_keys(chambres)

        time.sleep(1)  # laisser le site traiter

        # 5. Cliquer sur le bouton rouge (Soumettre)
        bouton = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        bouton.click()

        # 6. Attendre les résultats
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="revenue"]')))
        time.sleep(1)

        # 7. Extraction des résultats
        revenus_mensuels = driver.find_element(By.XPATH, "//div[contains(text(),'Revenus annuels')]/following-sibling::div").text.strip()
        taux_25 = driver.find_element(By.XPATH, "//div[contains(text(),'25e percentile')]/following-sibling::div").text.strip()
        taux_50 = driver.find_element(By.XPATH, "//div[contains(text(),'50e percentile')]/following-sibling::div").text.strip()
        taux_75 = driver.find_element(By.XPATH, "//div[contains(text(),'75e percentile')]/following-sibling::div").text.strip()
        taux_occupation = driver.find_element(By.XPATH, "//div[contains(text(),'Occupation moyenne')]/following-sibling::div").text.strip()
        nombre_annonces = driver.find_element(By.XPATH, "//div[contains(text(),\"Nombre d'annonces\")]/following-sibling::div").text.strip()

        # 8. Nettoyage
        driver.quit()

        return jsonify({
            "revenus_mensuels": revenus_mensuels,
            "taux_journalier_moyen": {
                "25e": taux_25,
                "50e": taux_50,
                "75e": taux_75
            },
            "occupation_moyenne": taux_occupation,
            "nombre_annonces": nombre_annonces
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Lancement du serveur Flask...")
    app.run(host="0.0.0.0", port=5000)
