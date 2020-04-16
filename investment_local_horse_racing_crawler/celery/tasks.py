import os
from celery import Celery
from celery_slack import Slackify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from billiard import Process


app = Celery("tasks")
app.conf.update(
    enable_utc=False,
    timezone=os.getenv("TZ"),
    broker_url=os.getenv("CELERY_REDIS_URL"),
    result_backend=os.getenv("CELERY_REDIS_URL"),
    worker_concurrency=1,
)


if os.getenv("CELERY_SLACK_WEBHOOK"):
    slack_app = Slackify(app, os.getenv("CELERY_SLACK_WEBHOOK"))


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


@app.task
def health():
    return "ok"


crawler = CrawlerScript()


@app.task
def crawl(args):
    start_url = args.get("start_url", "https://www.oddspark.com/keiba/KaisaiCalendar.do")
    recrawl_period = args.get("recrawl_period", "all")
    recrawl_race_id = args.get("recrawl_race_id", None)
    recache_race = args.get("recache_race", False)
    recache_horse = args.get("recache_horse", False)

    crawler.crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)
