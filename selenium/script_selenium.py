import time
import csv
import os
import json  
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Chronomètre début ===
start_time = time.time()

# === Configuration Firefox Headless ===
options = Options()
options.add_argument("--headless")

# === Définir le chemin vers GeckoDriver (⚠️ modifie selon ton système) ===
driver_path = r'C:\selenium\drivers\geckodriver.exe'# <--chemin du driver!
service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

# === Aller à la page principale ===
base_url = "https://www.anime-planet.com/anime/top-anime"
driver.get(base_url)
print("📥 Chargement du top 100 animes...")

# === Collecte des liens ===
anime_links = []
rows = driver.find_elements(By.CSS_SELECTOR, "table.pure-table tbody tr")
for row in rows:
    try:
        link = row.find_element(By.CSS_SELECTOR, "td.tableTitle a").get_attribute("href")
        anime_links.append(link)
    except Exception as e:
        print("❌ Erreur récupération lien :", e)

print(f"🔗 Total de liens collectés : {len(anime_links)}")

# === Données collectées ===
animes = []

for index, link in enumerate(anime_links, start=1):
    driver.get(link)
    try:
        # Titre
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))).text.strip()

        # Rang
        rank = driver.find_element(By.CSS_SELECTOR, "div.pure-1.md-1-5:nth-child(2)").text.strip()

        # Note
        rating = driver.find_element(By.CSS_SELECTOR, "div.avgRating").text.strip()

        # Nb épisodes
        episodes_text = driver.find_element(By.CSS_SELECTOR, "div.pure-1.md-1-5:nth-child(1)").text.strip()
        episodes = episodes_text.split("(")[-1].split("eps")[0].strip() if "eps" in episodes_text else "?"

        # Description
        try:
            desc = driver.find_element(By.CSS_SELECTOR, "div.entrySynopsis > div > p").text.strip()
        except:
            desc = "Non disponible"

        # Ajout
        anime = {
            "rang": rank,
            "titre": title,
            "note": rating,
            "episodes": episodes,
            "description": desc
        }
        animes.append(anime)
        print(f"✅ {index:03d} - {title}")
    except Exception as e:
        print(f"❌ {index:03d} - Erreur sur {link} : {e}")

# === Enregistrement CSV ===
os.makedirs("output", exist_ok=True)
with open("output/top_animes.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["rang", "titre", "note", "episodes", "description"])
    writer.writeheader()
    writer.writerows(animes)
import json  # en haut du fichier s'il n'y est pas déjà

# === Enregistrement JSON ===
with open("output/top_animes.json", "w", encoding="utf-8") as f_json:
    json.dump(animes, f_json, ensure_ascii=False, indent=4)
print(f"📄 Données JSON sauvegardées dans 'output/top_animes.json'")

# === Temps final ===
end_time = time.time()
print(f"\n✅ Extraction terminée. {len(animes)} animes sauvegardés dans 'output/top_animes.csv'")
print(f"⏱️ Durée totale : {round(end_time - start_time, 2)} secondes")

# Fermeture du navigateur
driver.quit()

