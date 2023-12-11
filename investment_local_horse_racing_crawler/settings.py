import logging
import os
from distutils.util import strtobool

BOT_NAME = 'investment_local_horse_racing_crawler'
USER_AGENT = os.environ.get("USER_AGENT", "local_horse_racing_crawler/1.0 (+https://github.com/u6k/investment-local-horse-racing-crawler)")
CRAWL_HTTP_PROXY = os.environ.get("CRAWL_HTTP_PROXY")

SPIDER_MODULES = ['investment_local_horse_racing_crawler.spiders']
NEWSPIDER_MODULE = 'investment_local_horse_racing_crawler.spiders'

ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

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

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_GZIP = True

SPIDER_CONTRACTS = {
    "investment_local_horse_racing_crawler.contracts.CalendarContract": 10,
    "investment_local_horse_racing_crawler.contracts.KaisaiRaceListContract": 10,
    "investment_local_horse_racing_crawler.contracts.OneDayRaceListContract": 10,
    "investment_local_horse_racing_crawler.contracts.RaceDenmaContract": 10,
    "investment_local_horse_racing_crawler.contracts.RaceResultContract": 10,
    "investment_local_horse_racing_crawler.contracts.HorseContract": 10,
    "investment_local_horse_racing_crawler.contracts.JockeyContract": 10,
    "investment_local_horse_racing_crawler.contracts.TrainerContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsWinPlaceContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsQuinellaContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsExactaContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsQuinellaPlaceContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsTrioContract": 10,
    "investment_local_horse_racing_crawler.contracts.OddsTrifectaContract": 10,
}

logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)

AWS_ENDPOINT_URL = os.environ["AWS_ENDPOINT_URL"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_S3_CACHE_BUCKET = os.environ["AWS_S3_CACHE_BUCKET"]
AWS_S3_CACHE_FOLDER = os.environ["AWS_S3_CACHE_FOLDER"]

RECACHE_RACE = strtobool(os.environ.get("RECACHE_RACE", "False"))
RECACHE_DATA = strtobool(os.environ.get("RECACHE_DATA", "False"))
