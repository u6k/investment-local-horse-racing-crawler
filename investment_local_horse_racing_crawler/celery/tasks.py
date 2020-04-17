import os
from celery import Celery
from celery_slack import Slackify
from celery.schedules import crontab
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from billiard import Process
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime, timedelta
import re
import requests
import json


app = Celery("tasks")
app.conf.update(
    enable_utc=False,
    timezone=os.getenv("TZ"),
    broker_url=os.getenv("CELERY_REDIS_URL"),
    result_backend=os.getenv("CELERY_REDIS_URL"),
    worker_concurrency=1,

    beat_schedule={
        "crawl_and_vote_everyday": {
            "task": "investment_local_horse_racing_crawler.celery.tasks.crawl_and_vote",
            "schedule": crontab(hour=10, minute=0),
        }
    }
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


@app.task
def crawl_and_vote():
    # crawl
    start_url = "https://www.oddspark.com/keiba/KaisaiCalendar.do"
    recrawl_period = 1
    recrawl_race_id = None
    recache_race = True
    recache_horse = False

    crawler.crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)

    # find race info
    race_infos = None

    settings = get_project_settings()

    db_conn = psycopg2.connect(
        host=settings.get("DB_HOST"),
        port=settings.get("DB_PORT"),
        dbname=settings.get("DB_DATABASE"),
        user=settings.get("DB_USERNAME"),
        password=settings.get("DB_PASSWORD"),
    )
    db_conn.autocommit = False
    db_conn.set_client_encoding("utf-8")
    db_conn.cursor_factory = DictCursor
    try:
        db_cursor = db_conn.cursor()
        try:

            end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0, 0) + timedelta(days=1)
            start_date = end_date - timedelta(days=1)

            db_cursor.execute("select race_id, start_datetime, place_name, race_name from race_info where %s <= start_datetime and start_datetime < %s order by start_datetime", (start_date, end_date))
            race_infos = db_cursor.fetchall()

        finally:
            db_cursor.close()
    finally:
        db_conn.close()

    # vote
    for race_info in race_infos:
        print(race_info)

        race_id_re = re.match("^raceDy=([0-9]+)&opTrackCd=([0-9]+)&raceNb=([0-9]+)&sponsorCd=([0-9]+)$", race_info["race_id"])
        if not race_id_re:
            raise RuntimeError("race_id unknown pattern")

        kaisaiBi = race_id_re.group(1)
        joCode = race_id_re.group(2)
        raceNo = race_id_re.group(3)
        vote_id = f"kaisaiBi={kaisaiBi}&joCode={joCode}&raceNo={raceNo}"
        print(vote_id)

        eta = race_info["start_datetime"] - timedelta(minutes=5)

        params = json.dumps({
            "args": [race_info["race_id"], vote_id],
            "eta": eta.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        })
        print(params)

        resp = requests.post(url=settings.get("CELERY_VOTE_API"), data=params, auth=(settings.get("CELERY_USERNAME"), settings.get("CELERY_PASSWORD")))
        print(resp.status_code)
        print(resp.text)
