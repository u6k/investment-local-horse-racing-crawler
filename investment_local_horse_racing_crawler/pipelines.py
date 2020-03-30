# -*- coding: utf-8 -*-


from datetime import datetime
import logging
import psycopg2
from psycopg2.extras import DictCursor
import re
from scrapy.exceptions import DropItem

from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem, OddsWinPlaceItem


logger = logging.getLogger(__name__)


class PostgreSQLPipeline(object):
    def __init__(self, db_host, db_port, db_database, db_username, db_password):
        logger.debug("#init: start: db_host=%s, db_port=%s, db_database=%s, db_username=%s" % (db_host, db_port, db_database, db_username))

        self.db_host = db_host
        self.db_port = db_port
        self.db_database = db_database
        self.db_username = db_username
        self.db_password = db_password

    @classmethod
    def from_crawler(cls, crawler):
        logger.debug("#from_crawler")

        return cls(
            db_host=crawler.settings.get("DB_HOST"),
            db_port=crawler.settings.get("DB_PORT"),
            db_database=crawler.settings.get("DB_DATABASE"),
            db_username=crawler.settings.get("DB_USERNAME"),
            db_password=crawler.settings.get("DB_PASSWORD")
        )

    def open_spider(self, spider):
        logger.debug("#open_spider: start: spider=%s" % spider)

        self.db_conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_database,
            user=self.db_username,
            password=self.db_password
        )
        self.db_conn.autocommit = False
        self.db_conn.set_client_encoding("utf-8")
        self.db_conn.cursor_factory = DictCursor
        self.db_cursor = self.db_conn.cursor()

        logger.debug("#open_spider: database connected")

    def close_spider(self, spider):
        logger.debug("#close_spider: start")

        self.db_cursor.close()
        self.db_conn.close()

        logger.debug("#close_spider: database disconnected")

    def process_item(self, item, spider):
        logger.debug("#process_item: start: item=%s" % item)

        if isinstance(item, RaceInfoItem):
            new_item = self.process_race_info_item(item, spider)
        elif isinstance(item, RaceDenmaItem):
            new_item = self.process_race_denma_item(item, spider)
        elif isinstance(item, OddsWinPlaceItem):
            new_item = self.process_odds_win_place_item(item, spider)
        else:
            raise DropItem("Unknown item type")

        self.db_cursor.execute("select 1")
        results = self.db_cursor.fetchall()

        logger.debug("#process_item: database results=%s" % results)

        return new_item

    def process_race_info_item(self, item, spider):
        logger.info("#process_race_info_item: start: item=%s" % item)

        # Build item
        i = {}

        i["race_id"] = item["race_id"][0].strip()

        race_round_re = re.match("^R([0-9]+)$", item["race_round"][0].strip())
        if race_round_re:
            i["race_round"] = int(race_round_re.group(1))
        else:
            raise DropItem("Unknown pattern race_round")

        start_date_re = re.match("^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日", item["start_date"][0].strip())
        start_time_re = re.match("^発走時間 ([0-9]+):([0-9]+)$", item["start_time"][0].strip())
        if start_date_re and start_time_re:
            i["start_datetime"] = datetime(int(start_date_re.group(1)), int(start_date_re.group(2)), int(start_date_re.group(3)), int(start_time_re.group(1)), int(start_time_re.group(2)), 0)
        else:
            raise DropItem("Unknown pattern start_date, start_time")

        i["place_name"] = item["place_name"][0].strip()

        i["race_name"] = item["race_name"][0].strip()

        course_type_length_re = re.match("^(.+?)([0-9]+)m$", item["course_type_length"][0].strip())
        if course_type_length_re:
            i["course_type"] = course_type_length_re.group(1)
            i["course_length"] = int(course_type_length_re.group(2))
        else:
            raise DropItem("Unknown pattern course_type_length")

        weather_str = item["weather"][0].strip()
        if weather_str.startswith("/local/images/ico-tenki-1.gif"):
            i["weather"] = "晴れ"
        elif weather_str.startswith("/local/images/ico-tenki-2.gif"):
            i["weather"] = "くもり"
        elif weather_str.startswith("/local/images/ico-tenki-3.gif"):
            i["weather"] = "雨"
        elif weather_str.startswith("/local/images/ico-tenki-4.gif"):
            i["weather"] = "小雨"
        elif weather_str.startswith("/local/images/ico-tenki-5.gif"):
            i["weather"] = "かみなり"
        elif weather_str.startswith("/local/images/ico-tenki-6.gif"):
            i["weather"] = "雪"
        else:
            raise DropItem(f"Unknown pattern weather: {weather_str}")

        i["moisture"] = float(item["moisture"][0].strip().replace("%", ""))

        i["added_money"] = item["added_money"][0].strip()

        # Insert db
        self.db_cursor.execute("delete from race_info where race_id=%s", (i["race_id"],))
        self.db_cursor.execute("insert into race_info (race_id, race_round, start_datetime, place_name, race_name, course_type, course_length, weather, moisture, added_money) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i["race_id"], i["race_round"], i["start_datetime"], i["place_name"], i["race_name"], i["course_type"], i["course_length"], i["weather"], i["moisture"], i["added_money"]))
        self.db_conn.commit()

        return i

    def process_race_denma_item(self, item, spider):
        logger.info("#process_race_denma_item: start: item=%s" % item)

        # Build item
        i = {}

        i["race_id"] = item["race_id"][0].strip()

        i["bracket_number"] = int(item["bracket_number"][0].strip())

        i["horse_number"] = int(item["horse_number"][0].strip())

        horse_id_re = re.match("^.*lineageNb=([0-9]+)$", item["horse_id"][0].strip())
        if horse_id_re:
            i["horse_id"] = horse_id_re.group(1)
        else:
            raise DropItem("Unknown pattern horse_id")

        i["horse_weight"] = float(item["horse_weight"][0].strip())

        i["horse_weight_diff"] = float(item["horse_weight_diff"][0].strip())

        trainer_id_re = re.match("^.*trainerNb=([0-9]+)$", item["trainer_id"][0].strip())
        if trainer_id_re:
            i["trainer_id"] = trainer_id_re.group(1)
        else:
            raise DropItem("Unknown pattern trainer_id")

        jockey_id_re = re.match("^.*jkyNb=([0-9]+)$", item["jockey_id"][0].strip())
        if jockey_id_re:
            i["jockey_id"] = jockey_id_re.group(1)
        else:
            raise DropItem("Unknown pattern jockey_id")

        i["jockey_weight"] = float(item["jockey_weight"][0].strip())

        i["odds_win"] = float(item["odds_win"][0].strip())

        favorite_re = re.match("^\\(([0-9]+)人気\\)$", item["favorite"][2].strip())
        if favorite_re:
            i["favorite"] = int(favorite_re.group(1))
        else:
            raise DropItem("Unknown pattern favorite")

        i["race_denma_id"] = f"{i['race_id']}_{i['horse_id']}"

        # Insert db
        self.db_cursor.execute("delete from race_denma where race_denma_id=%s", (i["race_denma_id"],))
        self.db_cursor.execute("insert into race_denma (race_denma_id, race_id, bracket_number, horse_number, horse_id, horse_weight, horse_weight_diff, trainer_id, jockey_id, jockey_weight, odds_win, favorite) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i["race_denma_id"], i["race_id"], i["bracket_number"], i["horse_number"], i["horse_id"], i["horse_weight"], i["horse_weight_diff"], i["trainer_id"], i["jockey_id"], i["jockey_weight"], i["odds_win"], i["favorite"]))
        self.db_conn.commit()

        return i

    def process_odds_win_place_item(self, item, spider):
        logger.info("#process_odds_win_place_item: start: item=%s" % item)

        # Build item
        i = {}

        i["race_id"] = item["race_id"][0].strip()

        i["horse_number"] = int(item["horse_number"][0].strip())

        horse_id_re = re.match("^.*lineageNb=([0-9]+)$", item["horse_id"][0].strip())
        if horse_id_re:
            i["horse_id"] = horse_id_re.group(1)
        else:
            raise DropItem("Unknown pattern horse_id")

        i["odds_win"] = float(item["odds_win"][0].strip())

        i["odds_place_min"] = float(item["odds_place_min"][0].strip())

        i["odds_place_max"] = float(item["odds_place_max"][0].strip())

        i["odds_win_place_id"] = f"{i['race_id']}_{i['horse_id']}"

        # Insert db
        self.db_cursor.execute("delete from odds_win where odds_win_id=%s", (i["odds_win_place_id"],))
        self.db_cursor.execute("insert into odds_win (odds_win_id, race_id, horse_number, horse_id, odds_win) values (%s, %s, %s, %s, %s)", (i["odds_win_place_id"], i["race_id"], i["horse_number"], i["horse_id"], i["odds_win"]))

        self.db_cursor.execute("delete from odds_place where odds_place_id=%s", (i["odds_win_place_id"],))
        self.db_cursor.execute("insert into odds_place (odds_place_id, race_id, horse_number, horse_id, odds_place_min, odds_place_max) values (%s, %s, %s, %s, %s, %s)", (i["odds_win_place_id"], i["race_id"], i["horse_number"], i["horse_id"], i["odds_place_min"], i["odds_place_max"]))

        self.db_conn.commit()

        return i
