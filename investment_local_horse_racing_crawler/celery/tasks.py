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
        settings_ex = {
            "APP_RECRAWL_RACE": "sponsorCd=20&raceDy=20200402&opTrackCd=42&raceNb=2"
        }
        settings.update(settings_ex)

        self.crawler = CrawlerProcess(settings)

    def _crawl(self):
        self.crawler.crawl("local_horse_racing")
        self.crawler.start()
        self.crawler.stop()

    def crawl(self):
        process = Process(target=self._crawl)
        process.start()
        process.join()


@app.task
def health():
    return "ok"


crawler = CrawlerScript()


@app.task
def crawl():
    crawler.crawl()
