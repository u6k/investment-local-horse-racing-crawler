import os
from celery import Celery
from celery_slack import Slackify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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


@app.task
def health():
    return "ok"


@app.task
def crawl():
    settings = get_project_settings()

    process = CrawlerProcess(settings)
    process.crawl("local_horse_racing")
    process.start()
