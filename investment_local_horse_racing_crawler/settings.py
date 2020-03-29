# -*- coding: utf-8 -*-


import os
import logging


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

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'investment_local_horse_racing_crawler.pipelines.InvestmentLocalHorseRacingCrawlerPipeline': 300,
# }

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = 'investment_local_horse_racing_crawler.middlewares.S3CacheStorage'

SPIDER_CONTRACTS = {
    "investment_local_horse_racing_crawler.contracts.ScheduleListContract": 10,
}

logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)

S3_ENDPOINT = os.environ["S3_ENDPOINT"]
S3_REGION = os.environ["S3_REGION"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_FOLDER = os.environ["S3_FOLDER"]
