BOT_NAME = 'animeplanet_scrapy'

SPIDER_MODULES = ['animeplanet_scrapy.spiders']
NEWSPIDER_MODULE = 'animeplanet_scrapy.spiders'

ROBOTSTXT_OBEY = False

LOG_LEVEL = 'INFO'
FEED_EXPORT_ENCODING = 'utf-8'

# User-Agent personnalisé pour contourner le blocage 403
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
}

# Facultatif : anti-ban (ralentir les requêtes)
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

ITEM_PIPELINES = {
    'animeplanet_scrapy.pipelines.AnimeplanetScrapyPipeline': 300,
}
