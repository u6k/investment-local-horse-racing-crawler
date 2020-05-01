from flask import Flask, request

from investment_local_horse_racing_crawler.scrapy import crawler
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


app = Flask(__name__)


@app.route("/api/health")
def health():
    logger.info("#health: start")

    return "ok"


@app.route("/api/crawl", methods=["POST"])
def crawl():
    logger.info("#crawl: start")

    args = request.get_json()
    logger.info("#crawl: args={args}")

    start_url = args.get("start_url", "https://www.oddspark.com/keiba/KaisaiCalendar.do")
    recrawl_period = args.get("recrawl_period", "all")
    recrawl_race_id = args.get("recrawl_race_id", None)
    recache_race = args.get("recache_race", False)
    recache_horse = args.get("recache_horse", False)

    crawler.crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)

    return "ok"
