# -*- coding: utf-8 -*-


import os
import logging
from datetime import datetime, timedelta
from distutils.util import strtobool


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
    "investment_local_horse_racing_crawler.scrapy.contracts.ScheduleListContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceRefundListContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceDenmaContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.OddsWinContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.RaceResultContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.HorseContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.JockeyContract": 10,
    "investment_local_horse_racing_crawler.scrapy.contracts.TrainerContract": 10,
}

logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)

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


APP_RECRAWL_PERIOD = os.getenv("APP_RECRAWL_PERIOD")
if APP_RECRAWL_PERIOD == "all":
    APP_RECRAWL_PERIOD = 100000
APP_RECRAWL_PERIOD = int(APP_RECRAWL_PERIOD)
APP_RECRAWL_END_DATE = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0, 0) + timedelta(days=1)
APP_RECRAWL_START_DATE = APP_RECRAWL_END_DATE - timedelta(days=APP_RECRAWL_PERIOD)

APP_RECRAWL_RACE = os.getenv("APP_RECRAWL_RACE", "")

APP_RECACHE_RACE = strtobool(os.getenv("APP_RECACHE_RACE", "False"))
APP_RECACHE_HORSE = strtobool(os.getenv("APP_RECACHE_HORSE", "False"))
