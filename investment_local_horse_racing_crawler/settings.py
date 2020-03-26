# -*- coding: utf-8 -*-

BOT_NAME = 'investment_local_horse_racing_crawler'
USER_AGENT = "local_horse_racing_crawler/1.0 (+https://github.com/u6k/investment-local-horse-racing-crawler)"

SPIDER_MODULES = ['investment_local_horse_racing_crawler.spiders']
NEWSPIDER_MODULE = 'investment_local_horse_racing_crawler.spiders'


ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0

DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 10

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'investment_local_horse_racing_crawler.middlewares.InvestmentLocalHorseRacingCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'investment_local_horse_racing_crawler.middlewares.InvestmentLocalHorseRacingCrawlerDownloaderMiddleware': 543,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'investment_local_horse_racing_crawler.pipelines.InvestmentLocalHorseRacingCrawlerPipeline': 300,
# }

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
