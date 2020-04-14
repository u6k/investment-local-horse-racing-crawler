import os
from celery import Celery
from celery_slack import Slackify


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
def hello():
    return "hello"
