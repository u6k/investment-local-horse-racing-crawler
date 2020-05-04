from datetime import datetime, timedelta
from dateutil.parser import parse
import os
import json
import requests
from flask import Flask, request, g
import psycopg2
from psycopg2.extras import DictCursor

from investment_local_horse_racing_crawler import VERSION
from investment_local_horse_racing_crawler.scrapy import crawler
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


app = Flask(__name__)


@app.route("/api/health")
def health():
    logger.info("#health: start")

    result = {"version": VERSION}

    return result


@app.route("/api/crawl", methods=["POST"])
def crawl():
    logger.info("#crawl: start")

    args = request.get_json()
    logger.debug(f"#crawl: args={args}")

    start_url = args.get("start_url", "https://www.oddspark.com/keiba/KaisaiCalendar.do")
    recrawl_period = args.get("recrawl_period", "all")
    recrawl_race_id = args.get("recrawl_race_id", None)
    recache_race = args.get("recache_race", False)
    recache_horse = args.get("recache_horse", False)

    _crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)

    return "ok"


@app.route("/api/schedule_crawl_vote_close", methods=["POST"])
def schedule_crawl_vote_close():
    logger.info("#schedule_crawl_vote_close: start")

    args = request.get_json()
    logger.debug(f"#schedule_crawl_vote_close: args={args}")

    target_date = parse(args.get("target_date", datetime.today().strftime("%Y-%m-%d")))
    start_date = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, 0)
    end_date = start_date + timedelta(days=1)

    _schedule_crawl_vote_close(start_date, end_date)

    return "ok"


def _get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD")
        )
        g.db.autocommit = False
        g.db.set_client_encoding("utf-8")
        g.db.cursor_factory = DictCursor

    return g.db


@app.teardown_appcontext
def _teardown_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def _crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse):
    logger.debug(f"#_crawl: start: start_url={start_url}, recrawl_period={recrawl_period}, recrawl_race_id={recrawl_race_id}, recache_race={recache_race}, recache_horse={recache_horse}")

    crawler.crawl(start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)


def _schedule_crawl_vote_close(start_date, end_date):
    logger.debug(f"#_schedule_crawl_vote_close: start_date={start_date}, end_date={end_date}")

    db_cursor = _get_db().cursor()
    try:

        db_cursor.execute("select race_id, start_datetime, place_name, race_name from race_info where start_datetime >= %s and start_datetime < %s order by start_datetime", (start_date, end_date))
        for row in db_cursor.fetchall():
            logger.debug(f"#_schedule_crawl_vote_close: row={row}")

            url = os.getenv("API_CRAWL_AND_VOTE_URL")
            headers = {
                "Content-Type": "application/json",
                "X-Rundeck-Auth-Token": os.getenv("API_RUNDECK_AUTH_TOKEN")
            }
            params = json.dumps({
                "runAtTime": (row["start_datetime"] - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
                "options": {
                    "RACE_ID": row["race_id"]
                }
            })
            logger.debug(f"#_schedule_crawl_vote_close: crawl_and_vote: url={url}, params={params}")

            resp = requests.post(url=url, headers=headers, data=params)
            logger.debug(f"#_schedule_crawl_vote_close: crawl_and_vote: status_code={resp.status_code}, body={resp.text}")

            url = os.getenv("API_CRAWL_AND_CLOSE_URL")
            params = json.dumps({
                "runAtTime": (row["start_datetime"] + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
                "options": {
                    "RACE_ID": row["race_id"]
                }
            })
            logger.debug(f"#_schedule_crawl_vote_close: crawl_and_close: url={url}, params={params}")

            resp = requests.post(url=url, headers=headers, data=params)
            logger.debug(f"#_schedule_crawl_vote_close: crawl_and_close: status_code={resp.status_code}, body={resp.text}")

    finally:
        db_cursor.close()
