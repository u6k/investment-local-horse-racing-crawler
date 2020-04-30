from flask import Flask, request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from billiard import Process

from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


app = Flask(__name__)


class CrawlerScript():
    def __init__(self):
        settings = get_project_settings()
        self.crawler = CrawlerProcess(settings, install_root_handler=False)

    def _crawl(self, start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse):
        self.crawler.crawl("local_horse_racing", start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse):
        process = Process(target=self._crawl, kwargs={"start_url": start_url, "recrawl_period": recrawl_period, "recrawl_race_id": recrawl_race_id, "recache_race": recache_race, "recache_horse": recache_horse})
        process.start()
        process.join()


crawler = CrawlerScript()


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
