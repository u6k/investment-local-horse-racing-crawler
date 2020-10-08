# TODO: 削除する

from datetime import datetime, timedelta
from dateutil.parser import parse
import os
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
    start_date = args.get("start_date", "1900-01-01")
    end_date = args.get("end_date", "2100-01-01")
    recache_race = args.get("recache_race", False)
    recache_horse = args.get("recache_horse", False)

    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    _crawl(start_url, start_date, end_date, recache_race, recache_horse)

    return {"result": True}


@app.route("/api/schedule_vote_close", methods=["POST"])
def schedule_vote_close():
    logger.info("#schedule_vote_close: start")

    args = request.get_json()
    logger.debug(f"#schedule_vote_close: args={args}")

    target_date = parse(args.get("target_date", datetime.today().strftime("%Y-%m-%d")))
    start_date = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, 0)
    end_date = start_date + timedelta(days=1)

    scheduled_races = _schedule_vote_close(start_date, end_date)
    logger.debug(f"#schedule_vote_close: scheduled_races={scheduled_races}")

    return scheduled_races


def get_db():
    db = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    db.autocommit = False
    db.set_client_encoding("utf-8")
    db.cursor_factory = DictCursor

    return db


def _get_db():
    if "db" not in g:
        g.db = get_db()

    return g.db


@app.teardown_appcontext
def _teardown_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def _crawl(start_url, start_date, end_date, recache_race, recache_horse):
    logger.debug(f"#_crawl: start: start_url={start_url}, start_date={start_date}, end_date={end_date}, recache_race={recache_race}, recache_horse={recache_horse}")

    crawler.crawl(start_url, start_date, end_date, recache_race, recache_horse)


def _schedule_vote_close(start_date, end_date):
    logger.debug(f"#_schedule_vote_close: start_date={start_date}, end_date={end_date}")

    scheduled_races = {"races": []}
    with _get_db().cursor() as db_cursor:
        db_cursor.execute("select race_id, start_datetime, place_name, race_name from race_info where start_datetime >= %s and start_datetime < %s order by start_datetime, race_id", (start_date, end_date))
        for idx, row in enumerate(db_cursor.fetchall()):
            logger.debug(f"#_schedule_vote_close: idx={idx}, row={row}")

            url = os.getenv("API_SCHEDULE_VOTE_CLOSE_URL")
            headers = {
                "Content-Type": "application/json",
                "X-Rundeck-Auth-Token": os.getenv("API_RUNDECK_AUTH_TOKEN")
            }
            params = {
                "options": {
                    "RACE_ID": row["race_id"],
                    "START_DATETIME": row["start_datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
            logger.debug(f"#_schedule_vote_close: url={url}, params={params}")

            resp = requests.post(url=url, headers=headers, json=params)
            logger.debug(f"#_schedule_vote_close: status_code={resp.status_code}, body={resp.text}")

            scheduled_race = {
                "race_id": params["options"]["RACE_ID"],
                "start_datetime": params["options"]["START_DATETIME"],
            }
            scheduled_races["races"].append(scheduled_race)

    return scheduled_races
