import scrapy
from animeplanet_scrapy.items import AnimeItem
import time

class TopAnimesSpider(scrapy.Spider):
    name = "top_animes"
    allowed_domains = ["anime-planet.com"]
    start_urls = ["https://www.anime-planet.com/anime/top-anime"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

    def parse(self, response):
        rows = response.css("table.pure-table tbody tr")
        for row in rows:
            rank = row.css("td.tableRank::text").get(default="").strip()
            title_tag = row.css("td.tableTitle a")
            title = title_tag.css("::text").get(default="").strip()
            relative_url = title_tag.attrib.get("href")

            if relative_url:
                full_url = response.urljoin(relative_url)
                yield response.follow(
                    full_url,
                    callback=self.parse_anime,
                    meta={"rang": rank, "titre": title}
                )

    def parse_anime(self, response):
        item = AnimeItem()
        item["rang"] = response.meta["rang"]
        item["titre"] = response.meta["titre"]

        # Description
        item["description"] = response.css("div.entrySynopsis p::text").get(default="").strip()

        # Note
        item["note"] = response.css("div.avgRating::attr(title)").get(default="").split(" out of")[0].strip()

        # Nb épisodes
        episodes_text = response.css("span.type::text").get(default="")
        if "eps" in episodes_text:
            item["episodes"] = episodes_text.split("(")[-1].split("eps")[0].strip()
        else:
            item["episodes"] = "?"

        yield item

    def closed(self, reason):
        duration = round(time.time() - self.start_time, 2)
        self.logger.info(f"⏱️ Durée totale d'exécution : {duration} secondes")
