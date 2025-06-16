import requests
from bs4 import BeautifulSoup
import csv
import time

# Démarrer le chrono
start = time.time()

# Liste pour stocker les données
animes = []

# Récupérer la page principale
print("Scraping en cours...")
url = "https://www.anime-planet.com/anime/top-anime"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Extraire les liens des animes
links = [a['href'] for a in soup.select('td.tableTitle a')]

for link in links[:10]:  # Limité à 10 pour l'exemple
    try:
        # Récupérer chaque page anime
        anime_page = requests.get(f"https://www.anime-planet.com{link}")
        anime_soup = BeautifulSoup(anime_page.text, 'html.parser')
        
        # Extraire les données
        data = {
            'titre': anime_soup.find('h1').text.strip(),
            'note': anime_soup.find('div', class_='avgRating').text.strip(),
            'episodes': anime_soup.find('div', class_='pure-1 md-1-5').text.split('(')[1].split('eps')[0].strip(),
            'description': anime_soup.find('div', class_='entrySynopsis').p.text.strip()
        }
        animes.append(data)
        print(f"Scrapé: {data['titre']}")
        
        time.sleep(1)  # Pause entre les requêtes
        
    except Exception as e:
        print(f"Erreur sur {link}: {e}")

# Sauvegarde CSV
with open('animes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['titre', 'note', 'episodes', 'description'])
    writer.writeheader()
    writer.writerows(animes)

print(f"Terminé en {time.time()-start:.2f}s. {len(animes)} animes sauvegardés.")