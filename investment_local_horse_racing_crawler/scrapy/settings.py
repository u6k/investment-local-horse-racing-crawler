import os


BOT_NAME = 'investment_local_horse_racing_crawler'
USER_AGENT = "local_horse_racing_crawler/1.0 (+https://github.com/u6k/investment-local-horse-racing-crawler)"

SPIDER_MODULES = ['investment_local_horse_racing_crawler.scrapy.spiders']
NEWSPIDER_MODULE = 'investment_local_horse_racing_crawler.scrapy.spiders'


ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0

DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 10

ITEM_PIPELINES = {
    'investment_local_horse_racing_crawler.scrapy.pipelines.PostgreSQLPipeline': 300,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = 'investment_local_horse_racing_crawler.scrapy.middlewares.S3CacheStorage'

SPIDER_CONTRACTS = {
    "investment_local_horse_racing_crawler.scrapy.contracts.CalendarContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.ScheduleListContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.OneDayRaceListContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceRefundListContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceDenmaContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.OddsWinContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceResultContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.HorseContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.JockeyContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.TrainerContract": 10,
}

S3_ENDPOINT = os.environ["S3_ENDPOINT"]
S3_REGION = os.environ["S3_REGION"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_FOLDER = os.environ["S3_FOLDER"]

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_DATABASE = os.environ["DB_DATABASE"]
