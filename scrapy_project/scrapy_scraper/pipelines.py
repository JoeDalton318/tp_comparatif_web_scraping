import csv
import json
import os
import shutil

class AnimeplanetScrapyPipeline:
    def open_spider(self, spider):
        # Suppression dossier data si déjà existant
        if os.path.exists("data"):
            shutil.rmtree("data")
        os.makedirs("data", exist_ok=True)

        self.items = []

        self.csv_file = open("data/animes.csv", "w", newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csv_file, fieldnames=["rang", "titre", "note", "episodes", "description"])
        self.writer.writeheader()

    def process_item(self, item, spider):
        item["titre"] = item.get("titre", "").strip()
        item["description"] = item.get("description", "").strip()
        item["episodes"] = item.get("episodes", "?").strip()

        self.writer.writerow(item)
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        self.csv_file.close()

        with open('data/animes.json', 'w', encoding='utf-8') as f_json:
            json.dump(self.items, f_json, ensure_ascii=False, indent=4)
