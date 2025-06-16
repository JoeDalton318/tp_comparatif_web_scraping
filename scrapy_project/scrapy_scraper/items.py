import scrapy

class AnimeItem(scrapy.Item):
    rang = scrapy.Field()
    titre = scrapy.Field()
    note = scrapy.Field()
    episodes = scrapy.Field()
    description = scrapy.Field()
