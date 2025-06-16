# beautifulsoup/top_scraper_bs.py

import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

os.makedirs("raw_data", exist_ok=True)

start_time = time.time()

BASE_URLS = {
    "top_anime": "https://www.anime-planet.com/anime/top-anime",
    "top_manga": "https://www.anime-planet.com/manga/top-manga",
    "top_characters": "https://www.anime-planet.com/characters/top-loved",
    "season_winter_2025": "https://www.anime-planet.com/anime/seasons/winter-2025",
    "season_spring_2025": "https://www.anime-planet.com/anime/seasons/spring-2025",
    "season_fall_2024": "https://www.anime-planet.com/anime/seasons/fall-2024",
}


def extract_titles_from_page(url, is_character=False):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    if is_character:
        cards = soup.select("ul.cardDeck li.card")
        return [
            {
                "title": card.select_one("h3").text.strip(),
                "url": "https://www.anime-planet.com"
                + card.select_one("a").get("href"),
            }
            for card in cards[:20]
        ]

    else:
        cards = soup.select("ul.cardDeck li.card")
        return [
            {
                "title": card.select_one("h3").text.strip(),
                "url": "https://www.anime-planet.com"
                + card.select_one("a").get("href"),
                "type": card.select_one(".type")
                and card.select_one(".type").text.strip(),
                "nb_votes": card.select_one(".avgRating .tooltip")
                and card.select_one(".tooltip").text.strip(),
            }
            for card in cards[:20]
        ]


all_data = []

for label, url in BASE_URLS.items():
    is_char = "characters" in url
    data = extract_titles_from_page(url, is_character=is_char)
    for d in data:
        d["category"] = label
        all_data.append(d)

# Sauvegarde CSV
df = pd.DataFrame(all_data)
df.to_csv("beautifulsoup/top_20_bs.csv", index=False, encoding="utf-8-sig")
print("Fichier CSV généré : top_20_bs.csv")

# Sauvegarde JSON
df.to_json("raw_data/top_20_bs.json", orient="records", indent=2, force_ascii=False)

# Timer
end_time = time.time()
print(f"Données sauvegardées dans raw_data/ - Temps d'exécution : {end_time - start_time:.2f} secondes")