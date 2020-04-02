# -*- coding: utf-8 -*-


from datetime import datetime
import logging
import psycopg2
from psycopg2.extras import DictCursor
import re
from scrapy.exceptions import DropItem

from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem, OddsWinPlaceItem, RaceResultItem, RacePayoffItem, HorseItem, JockeyItem, TrainerItem


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
        elif isinstance(item, RaceResultItem):
            new_item = self.process_race_result_item(item, spider)
        elif isinstance(item, RacePayoffItem):
            new_item = self.process_race_payoff_item(item, spider)
        elif isinstance(item, HorseItem):
            new_item = self.process_horse_item(item, spider)
        elif isinstance(item, JockeyItem):
            new_item = self.process_jockey_item(item, spider)
        elif isinstance(item, TrainerItem):
            new_item = self.process_trainer_item(item, spider)
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

        logger.debug(f"#process_race_info_item: build item: {i}")

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

        logger.debug(f"#process_race_denma_item: build item: {i}")

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

        logger.debug(f"#process_odds_win_place_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from odds_win where odds_win_id=%s", (i["odds_win_place_id"],))
        self.db_cursor.execute("insert into odds_win (odds_win_id, race_id, horse_number, horse_id, odds_win) values (%s, %s, %s, %s, %s)", (i["odds_win_place_id"], i["race_id"], i["horse_number"], i["horse_id"], i["odds_win"]))

        self.db_cursor.execute("delete from odds_place where odds_place_id=%s", (i["odds_win_place_id"],))
        self.db_cursor.execute("insert into odds_place (odds_place_id, race_id, horse_number, horse_id, odds_place_min, odds_place_max) values (%s, %s, %s, %s, %s, %s)", (i["odds_win_place_id"], i["race_id"], i["horse_number"], i["horse_id"], i["odds_place_min"], i["odds_place_max"]))

        self.db_conn.commit()

        return i

    def process_race_result_item(self, item, spider):
        logger.info("#process_race_result_item: start: item=%s" % item)

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

        i["result"] = int(item["result"][0].strip())

        arrival_time_str = item["arrival_time"][0].strip()
        arrival_time_parts = re.split("[:\\.]", arrival_time_str)
        if len(arrival_time_parts) == 3:
            i["arrival_time"] = int(arrival_time_parts[0]) * 60 + int(arrival_time_parts[1]) + int(arrival_time_parts[2]) / 10.0
        elif len(arrival_time_parts) == 2:
            i["arrival_time"] = int(arrival_time_parts[0]) + int(arrival_time_parts[1]) / 10.0
        else:
            raise DropItem("Unknown pattern arrival_time")

        i["race_result_id"] = f"{i['race_id']}_{i['horse_id']}"

        logger.debug(f"#process_race_result_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from race_result where race_result_id=%s", (i["race_result_id"],))
        self.db_cursor.execute("insert into race_result (race_result_id, race_id, bracket_number, horse_number, horse_id, result, arrival_time) values (%s, %s, %s, %s, %s, %s, %s)", (i["race_result_id"], i["race_id"], i["bracket_number"], i["horse_number"], i["horse_id"], i["result"], i["arrival_time"]))

        self.db_conn.commit()

        return i

    def process_race_payoff_item(self, item, spider):
        logger.info("#process_race_payoff_item: start: item=%s" % item)

        # Build item
        i = {}

        i["race_id"] = item["race_id"][0].strip()

        horse_number_parts = item["horse_number"][0].split("-")
        if len(horse_number_parts) == 1:
            i["horse_number_1"] = int(horse_number_parts[0])
            i["horse_number_2"] = None
            i["horse_number_3"] = None
        elif len(horse_number_parts) == 2:
            i["horse_number_1"] = int(horse_number_parts[0])
            i["horse_number_2"] = int(horse_number_parts[1])
            i["horse_number_3"] = None
        elif len(horse_number_parts) == 3:
            i["horse_number_1"] = int(horse_number_parts[0])
            i["horse_number_2"] = int(horse_number_parts[1])
            i["horse_number_3"] = int(horse_number_parts[2])
        else:
            raise DropItem("Unknown pattern horse_number")

        if item["payoff_type"][0] == '単勝':
            i["payoff_type"] = "win"
        elif item["payoff_type"][0] == '複勝':
            i["payoff_type"] = "place"
        elif item["payoff_type"][0] == '枠連':
            i["payoff_type"] = "bracket_quinella"
        elif item["payoff_type"][0] == '馬連':
            i["payoff_type"] = "quinella"
        elif item["payoff_type"][0] == '馬単':
            i["payoff_type"] = "exacta"
        elif item["payoff_type"][0] == 'ワイド':
            i["payoff_type"] = "quinella_place"
        elif item["payoff_type"][0] == '3連複':
            i["payoff_type"] = "trio"
        elif item["payoff_type"][0] == '3連単':
            i["payoff_type"] = "trifecta"
        else:
            raise DropItem("Unknown pattern payoff_type")

        i["odds"] = int(item["odds"][0].replace(",", "").replace("円", "")) / 100.0

        i["favorite"] = int(item["favorite"][0].replace("番人気", ""))

        i["race_payoff_id"] = f"{i['race_id']}_{i['payoff_type']}_{item['horse_number'][0]}"

        logger.debug(f"#process_race_payoff_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from race_payoff where race_payoff_id=%s", (i["race_payoff_id"],))
        self.db_cursor.execute("insert into race_payoff (race_payoff_id, race_id, payoff_type, horse_number_1, horse_number_2, horse_number_3, odds, favorite) values (%s, %s, %s, %s, %s, %s, %s, %s)", (i["race_payoff_id"], i["race_id"], i["payoff_type"], i["horse_number_1"], i["horse_number_2"], i["horse_number_3"], i["odds"], i["favorite"]))

        self.db_conn.commit()

        return i

    def process_horse_item(self, item, spider):
        logger.info("#process_horse_item: start: item=%s" % item)

        # Build item
        i = {}

        horse_id_re = re.match("^lineageNb=([0-9]+)$", item["horse_id"][0].strip())
        if horse_id_re:
            i["horse_id"] = horse_id_re.group(1)
        else:
            raise DropItem("Unknown pattern horse_id")

        i["horse_name"] = item["horse_name"][0].strip()

        gender_age_parts = item["gender_age"][0].split("｜")
        i["gender"] = gender_age_parts[0].strip()

        age_re = re.match("^([0-9]+) 歳$", gender_age_parts[1].strip())
        if age_re:
            i["age"] = int(age_re.group(1))
        else:
            raise DropItem("Unknown pattern age")

        birthday_re = re.match("^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日$", item["birthday"][0].strip())
        if birthday_re:
            i["birthday"] = datetime(int(birthday_re.group(1)), int(birthday_re.group(2)), int(birthday_re.group(3)), 0, 0, 0)
        else:
            raise DropItem("Unknown pattern birthday")

        i['coat_color'] = item["coat_color"][0].strip()

        i['owner'] = item["owner"][0].strip()

        i['breeder'] = item["breeder"][0].strip()

        i['breeding_farm'] = item["breeding_farm"][0].strip()

        i['parent_horse_name_1'] = item["parent_horse_name_1"][0].strip()

        i['parent_horse_name_2'] = item["parent_horse_name_2"][0].strip()

        i['grand_parent_horse_name_1'] = item["grand_parent_horse_name_1"][0].strip()

        i['grand_parent_horse_name_2'] = item["grand_parent_horse_name_2"][0].strip()

        i['grand_parent_horse_name_3'] = item["grand_parent_horse_name_3"][0].strip()

        i['grand_parent_horse_name_4'] = item["grand_parent_horse_name_4"][0].strip()

        logger.debug(f"#process_horse_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from horse where horse_id=%s", (i["horse_id"],))
        self.db_cursor.execute("insert into horse (horse_id, horse_name, gender, age, birthday, coat_color, owner, breeder, breeding_farm, parent_horse_name_1, parent_horse_name_2, grand_parent_horse_name_1, grand_parent_horse_name_2, grand_parent_horse_name_3, grand_parent_horse_name_4) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i["horse_id"], i["horse_name"], i["gender"], i["age"], i["birthday"], i["coat_color"], i["owner"], i["breeder"], i["breeding_farm"], i["parent_horse_name_1"], i["parent_horse_name_2"], i["grand_parent_horse_name_1"], i["grand_parent_horse_name_2"], i["grand_parent_horse_name_3"], i["grand_parent_horse_name_4"]))

        self.db_conn.commit()

        return i

    def process_jockey_item(self, item, spider):
        logger.info("#process_jockey_item: start: item=%s" % item)

        # Build item
        i = {}

        jockey_id_re = re.match("^jkyNb=([0-9]+)$", item["jockey_id"][0].strip())
        if jockey_id_re:
            i["jockey_id"] = jockey_id_re.group(1)
        else:
            raise DropItem("Unknown pattern jockey_id")

        i["jockey_name"] = item["jockey_name"][0].strip()

        birthday_re = re.match("^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日$", item["birthday"][0].strip())
        if birthday_re:
            i["birthday"] = datetime(int(birthday_re.group(1)), int(birthday_re.group(2)), int(birthday_re.group(3)), 0, 0, 0)
        else:
            raise DropItem("Unknown pattern birthday")

        i["gender"] = item["gender"][0].strip()

        i["belong_to"] = item["belong_to"][0].strip()

        i["first_licensing_year"] = int(item["first_licensing_year"][0].strip().replace("年", ""))

        logger.debug(f"#process_jockey_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from jockey where jockey_id=%s", (i["jockey_id"],))
        self.db_cursor.execute("insert into jockey (jockey_id, jockey_name, birthday, gender, belong_to, first_licensing_year) values (%s, %s, %s, %s, %s, %s)", (i["jockey_id"], i["jockey_name"], i["birthday"], i["gender"], i["belong_to"], i["first_licensing_year"]))

        self.db_conn.commit()

        return i

    def process_trainer_item(self, item, spider):
        logger.info("#process_trainer_item: start: item=%s" % item)

        # Build item
        i = {}

        trainer_id_re = re.match("^trainerNb=([0-9]+)$", item["trainer_id"][0].strip())
        if trainer_id_re:
            i["trainer_id"] = trainer_id_re.group(1)
        else:
            raise DropItem("Unknown pattern trainer_id")

        i["trainer_name"] = item["trainer_name"][0].strip()

        birthday_re = re.match("^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日$", item["birthday"][0].strip())
        if birthday_re:
            i["birthday"] = datetime(int(birthday_re.group(1)), int(birthday_re.group(2)), int(birthday_re.group(3)), 0, 0, 0)
        else:
            raise DropItem("Unknown pattern birthday")

        i["gender"] = item["gender"][0].strip()

        i["belong_to"] = item["belong_to"][0].strip()

        logger.debug(f"#process_trainer_item: build item: {i}")

        # Insert db
        self.db_cursor.execute("delete from trainer where trainer_id=%s", (i["trainer_id"],))
        self.db_cursor.execute("insert into trainer (trainer_id, trainer_name, birthday, gender, belong_to) values (%s, %s, %s, %s, %s)", (i["trainer_id"], i["trainer_name"], i["birthday"], i["gender"], i["belong_to"]))

        self.db_conn.commit()

        return i
