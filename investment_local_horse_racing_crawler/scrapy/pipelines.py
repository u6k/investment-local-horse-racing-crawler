# -*- coding: utf-8 -*-


import psycopg2
from psycopg2.extras import DictCursor
from scrapy.exceptions import DropItem
import hashlib

from investment_local_horse_racing_crawler.scrapy.items import CalendarItem, RaceInfoMiniItem, RaceInfoItem, RaceDenmaItem, RaceResultItem, RaceCornerPassingOrderItem, RaceRefundItem, HorseItem, JockeyItem, TrainerItem, OddsWinPlaceItem, OddsQuinellaItem, OddsExactaItem, OddsQuinellaPlaceItem, OddsTrioItem, OddsTrifectaItem
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


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

        try:
            if isinstance(item, CalendarItem):
                self.process_calendar_item(item, spider)
            elif isinstance(item, RaceInfoMiniItem):
                self.process_race_info_mini_item(item, spider)
            elif isinstance(item, RaceInfoItem):
                self.process_race_info_item(item, spider)
            elif isinstance(item, RaceDenmaItem):
                self.process_race_denma_item(item, spider)
            elif isinstance(item, RaceResultItem):
                self.process_race_result_item(item, spider)
            elif isinstance(item, RaceCornerPassingOrderItem):
                self.process_race_corner_passing_order_item(item, spider)
            elif isinstance(item, RaceRefundItem):
                self.process_race_refund_item(item, spider)
            elif isinstance(item, HorseItem):
                self.process_horse_item(item, spider)
            elif isinstance(item, JockeyItem):
                self.process_jockey_item(item, spider)
            elif isinstance(item, TrainerItem):
                self.process_trainer_item(item, spider)
            elif isinstance(item, OddsWinPlaceItem):
                self.process_odds_win_place_item(item, spider)
            elif isinstance(item, OddsQuinellaItem):
                self.process_odds_quinella_item(item, spider)
            elif isinstance(item, OddsExactaItem):
                self.process_odds_exacta_item(item, spider)
            elif isinstance(item, OddsQuinellaPlaceItem):
                self.process_odds_quinella_place_item(item, spider)
            elif isinstance(item, OddsTrioItem):
                self.process_odds_trio_item(item, spider)
            elif isinstance(item, OddsTrifectaItem):
                self.process_odds_trifecta_item(item, spider)
            else:
                raise DropItem("Unknown item type")

            return item
        except Exception as e:
            logger.exception("except Exception")
            raise DropItem("except Exception") from e

    def process_calendar_item(self, item, spider):
        logger.info(f"#process_calendar_item: start: item={item}")

        # Delete db
        calendar_url = item["calendar_url"][0]

        logger.debug(f"#process_calendar_item: delete: calendar_url={calendar_url}")

        self.db_cursor.execute("delete from calendar_race_url where calendar_url=%s",
                               (calendar_url,))

        # Insert db
        for race_list_url in item["race_list_urls"]:
            id = hashlib.sha256((calendar_url + race_list_url).encode()).hexdigest()

            logger.debug(f"#process_calendar_item: insert: id={id}, calendar_url={calendar_url}, race_list_url={race_list_url}")

            self.db_cursor.execute("""insert into calendar_race_url (
                    id, calendar_url, race_list_url
                ) values (
                    %s, %s, %s
                )""", (id, calendar_url, race_list_url))

            self.db_conn.commit()

    def process_race_info_mini_item(self, item, spider):
        logger.info(f"#process_race_info_mini_item: start: item={item}")

        # Delete db
        race_list_url = item["race_list_url"][0]
        race_denma_url = item["race_denma_url"][0]

        logger.debug(f"#process_race_info_mini_item: delete: race_list_url={race_list_url}, race_denma_url={race_denma_url}")

        self.db_cursor.execute("delete from race_info_mini where race_list_url=%s and race_denma_url=%s",
                               (race_list_url, race_denma_url))

        # Insert db
        id = hashlib.sha256((race_list_url + race_denma_url).encode()).hexdigest()

        logger.debug(f"#process_race_info_mini_item: insert: id={id}, race_list_url={race_list_url}, race_denma_url={race_denma_url}")

        self.db_cursor.execute("""insert into race_info_mini (
                id, race_list_url, race_name, race_denma_url, course_length, start_time
            ) values (
                %s, %s, %s, %s, %s, %s
            )""", (
            id,
            race_list_url,
            item["race_name"][0] if "race_name" in item else None,
            race_denma_url,
            item["course_length"][0] if "course_length" in item else None,
            item["start_time"][0] if "start_time" in item else None,
        ))

        self.db_conn.commit()

    def process_race_info_item(self, item, spider):
        logger.info(f"#process_race_info_item: start: item={item}")

        # Delete db
        race_denma_url = item["race_denma_url"][0]

        logger.debug(f"#process_race_info_item: delete: race_denma_url={race_denma_url}")

        self.db_cursor.execute("delete from race_info where race_denma_url=%s",
                               (race_denma_url,))

        # Insert db
        id = hashlib.sha256(race_denma_url.encode()).hexdigest()

        logger.debug(f"#process_race_info_item: insert: id={id}, race_denma_url={race_denma_url}")

        self.db_cursor.execute("""insert into race_info (
                id,
                race_denma_url,
                race_round,
                race_name,
                start_date,
                place_name,
                course_type_length,
                start_time,
                weather_url,
                course_condition,
                moisture,
                prize_money
            ) values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
            id,
            race_denma_url,
            item["race_round"][0] if "race_round" in item else None,
            item["race_name"][0] if "race_name" in item else None,
            item["start_date"][0] if "start_date" in item else None,
            item["place_name"][0] if "place_name" in item else None,
            item["course_type_length"][0] if "course_type_length" in item else None,
            item["start_time"][0] if "start_time" in item else None,
            item["weather_url"][0] if "weather_url" in item else None,
            item["course_condition"][0] if "course_condition" in item else None,
            item["moisture"][0] if "moisture" in item else None,
            item["prize_money"][0] if "prize_money" in item else None
        ))

        self.db_conn.commit()

    def process_race_denma_item(self, item, spider):
        logger.info(f"#process_race_denma_item: start: item={item}")

        # Delete db
        race_denma_url = item["race_denma_url"][0]
        horse_url = item["horse_url"][0]

        logger.debug(f"#process_race_denma_item: delete: race_denma_url={race_denma_url}, horse_url={horse_url}")

        self.db_cursor.execute("delete from race_denma where race_denma_url=%s and horse_url=%s",
                               (race_denma_url, horse_url))

        # Insert db
        id = hashlib.sha256((race_denma_url + horse_url).encode()).hexdigest()

        logger.debug(f"#process_race_denma_item: insert: id={id}, race_denma_url={race_denma_url}, horse_url={horse_url}")

        self.db_cursor.execute("""insert into race_denma (
                id,
                race_denma_url,
                bracket_number,
                horse_number,
                horse_url,
                jockey_url,
                jockey_weight,
                trainer_url,
                odds_win_favorite,
                horse_weight,
                horse_weight_diff
            ) values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
            id,
            race_denma_url,
            item["bracket_number"][0] if "bracket_number" in item else None,
            item["horse_number"][0] if "horse_number" in item else None,
            horse_url,
            item["jockey_url"][0] if "jockey_url" in item else None,
            item["jockey_weight"][0] if "jockey_weight" in item else None,
            item["trainer_url"][0] if "trainer_url" in item else None,
            item["odds_win_favorite"][0] if "odds_win_favorite" in item else None,
            item["horse_weight"][0] if "horse_weight" in item else None,
            item["horse_weight_diff"][0] if "horse_weight_diff" in item else None
        ))

        self.db_conn.commit()

    def process_race_result_item(self, item, spider):
        logger.info(f"#process_race_result_item: start: item={item}")

        # Delete db
        race_result_url = item["race_result_url"][0]
        horse_url = item["horse_url"][0]
        id = hashlib.sha256((race_result_url + horse_url).encode()).hexdigest()

        logger.debug(f"#process_race_result_item: delete: id={id}, race_result_url={race_result_url}, horse_url={horse_url}")

        self.db_cursor.execute("delete from race_result where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_race_result_item: insert: id={id}, race_result_url={race_result_url}, horse_url={horse_url}")

        self.db_cursor.execute("""insert into race_result (
                id,
                race_result_url,
                result,
                bracket_number,
                horse_number,
                horse_url,
                arrival_time,
                arrival_margin,
                final_600_meters_time,
                corner_passing_order
            ) values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
            id,
            race_result_url,
            item["result"][0] if "result" in item else None,
            item["bracket_number"][0] if "bracket_number" in item else None,
            item["horse_number"][0] if "horse_number" in item else None,
            horse_url,
            item["arrival_time"][0] if "arrival_time" in item else None,
            item["arrival_margin"][0] if "arrival_margin" in item else None,
            item["final_600_meters_time"][0] if "final_600_meters_time" in item else None,
            item["corner_passing_order"][0] if "corner_passing_order" in item else None
        ))

        self.db_conn.commit()

    def process_race_corner_passing_order_item(self, item, spider):
        logger.info(f"#process_race_corner_passing_order_item: start: item={item}")

        # Delete db
        race_result_url = item["race_result_url"][0]
        corner_number = item["corner_number"][0]
        id = hashlib.sha256((race_result_url + corner_number).encode()).hexdigest()

        logger.debug(f"#process_race_corner_passing_order_item: delete: id={id}, race_result_url={race_result_url}, corner_number={corner_number}")

        self.db_cursor.execute("delete from race_corner_passing_order where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_race_corner_passing_order_item: insert: id={id}, race_result_url={race_result_url}, corner_number={corner_number}")

        self.db_cursor.execute("""insert into race_corner_passing_order (
                id,
                race_result_url,
                corner_number,
                passing_order
            ) values (
                %s, %s, %s, %s
            )""", (
            id,
            race_result_url,
            corner_number,
            item["passing_order"][0] if "passing_order" in item else None
        ))

        self.db_conn.commit()

    def process_race_refund_item(self, item, spider):
        logger.info(f"#process_race_refund_item: start: item={item}")

        # Delete db
        race_result_url = item["race_result_url"][0]
        betting_type = item["betting_type"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((race_result_url + betting_type + horse_number).encode()).hexdigest()

        logger.debug(f"#process_race_refund_item: delete: id={id}, race_result_url={race_result_url}, betting_type={betting_type}, horse_number={horse_number}")

        self.db_cursor.execute("delete from race_refund where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_race_refund_item: insert: id={id}, race_result_url={race_result_url}, betting_type={betting_type}, horse_number={horse_number}")

        self.db_cursor.execute("""insert into race_refund (
                id,
                race_result_url,
                betting_type,
                horse_number,
                refund_money,
                favorite
            ) values (
                %s, %s, %s, %s, %s, %s
            )""", (
            id,
            race_result_url,
            betting_type,
            horse_number,
            item["refund_money"][0] if "refund_money" in item else None,
            item["favorite"][0] if "favorite" in item else None
        ))

        self.db_conn.commit()

    def process_horse_item(self, item, spider):
        logger.info(f"#process_horse_item: start: item={item}")

        # Delete db
        horse_url = item["horse_url"][0]
        id = hashlib.sha256((horse_url).encode()).hexdigest()

        logger.debug(f"#process_horse_item: delete: id={id}, horse_url={horse_url}")

        self.db_cursor.execute("delete from horse where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_horse_item: insert: id={id}, horse_url={horse_url}")

        self.db_cursor.execute("""insert into horse (
                id,
                horse_url,
                horse_name,
                gender_age,
                birthday,
                coat_color,
                trainer_url,
                owner,
                breeder,
                breeding_farm,
                parent_horse_name_1,
                parent_horse_name_2,
                grand_parent_horse_name_1,
                grand_parent_horse_name_2,
                grand_parent_horse_name_3,
                grand_parent_horse_name_4
            ) values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
            id,
            horse_url,
            item["horse_name"][0] if "horse_name" in item else None,
            item["gender_age"][0] if "gender_age" in item else None,
            item["birthday"][0] if "birthday" in item else None,
            item["coat_color"][0] if "coat_color" in item else None,
            item["trainer_url"][0] if "trainer_url" in item else None,
            item["owner"][0] if "owner" in item else None,
            item["breeder"][0] if "breeder" in item else None,
            item["breeding_farm"][0] if "breeding_farm" in item else None,
            item["parent_horse_name_1"][0] if "parent_horse_name_1" in item else None,
            item["parent_horse_name_2"][0] if "parent_horse_name_2" in item else None,
            item["grand_parent_horse_name_1"][0] if "grand_parent_horse_name_1" in item else None,
            item["grand_parent_horse_name_2"][0] if "grand_parent_horse_name_2" in item else None,
            item["grand_parent_horse_name_3"][0] if "grand_parent_horse_name_3" in item else None,
            item["grand_parent_horse_name_4"][0] if "grand_parent_horse_name_4" in item else None
        ))

        self.db_conn.commit()

    def process_jockey_item(self, item, spider):
        logger.info(f"#process_jockey_item: start: item={item}")

        # Delete db
        jockey_url = item["jockey_url"][0]
        id = hashlib.sha256((jockey_url).encode()).hexdigest()

        logger.debug(f"#process_jockey_item: delete: id={id}, jockey_url={jockey_url}")

        self.db_cursor.execute("delete from jockey where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_jockey_item: insert: id={id}, jockey_url={jockey_url}")

        self.db_cursor.execute("""insert into jockey (
                id,
                jockey_url,
                jockey_name,
                birthday,
                gender,
                belong_to,
                trainer_url,
                first_licensing_year
            ) values (
                %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
            id,
            jockey_url,
            item["jockey_name"][0] if "jockey_name" in item else None,
            item["birthday"][0] if "birthday" in item else None,
            item["gender"][0] if "gender" in item else None,
            item["belong_to"][0] if "belong_to" in item else None,
            item["trainer_url"][0] if "trainer_url" in item else None,
            item["first_licensing_year"][0] if "first_licensing_year" in item else None
        ))

        self.db_conn.commit()

    def process_trainer_item(self, item, spider):
        logger.info(f"#process_trainer_item: start: item={item}")

        # Delete db
        trainer_url = item["trainer_url"][0]
        id = hashlib.sha256((trainer_url).encode()).hexdigest()

        logger.debug(f"#process_trainer_item: delete: id={id}, trainer_url={trainer_url}")

        self.db_cursor.execute("delete from trainer where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_trainer_item: insert: id={id}, trainer_url={trainer_url}")

        self.db_cursor.execute("""insert into trainer (
                id,
                trainer_url,
                trainer_name,
                birthday,
                gender,
                belong_to
            ) values (
                %s, %s, %s, %s, %s, %s
            )""", (
            id,
            trainer_url,
            item["trainer_name"][0] if "trainer_name" in item else None,
            item["birthday"][0] if "birthday" in item else None,
            item["gender"][0] if "gender" in item else None,
            item["belong_to"][0] if "belong_to" in item else None
        ))

        self.db_conn.commit()

    def process_odds_win_place_item(self, item, spider):
        logger.info(f"#process_odds_win_place_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_url = item["horse_url"][0]
        id = hashlib.sha256((odds_url + horse_url).encode()).hexdigest()

        logger.debug(f"#process_odds_win_place_item: delete: id={id}, odds_url={odds_url}, horse_url={horse_url}")

        self.db_cursor.execute("delete from odds_win_place where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_win_place_item: insert: id={id}, odds_url={odds_url}, horse_url={horse_url}")

        self.db_cursor.execute("""insert into odds_win_place (
                id,
                odds_url,
                horse_number,
                horse_url,
                odds_win,
                odds_place
            ) values (
                %s, %s, %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            item["horse_number"][0] if "horse_number" in item else None,
            horse_url,
            item["odds_win"][0] if "odds_win" in item else None,
            item["odds_place"][0] if "odds_place" in item else None,
        ))

        self.db_conn.commit()

    def process_odds_quinella_item(self, item, spider):
        logger.info(f"#process_odds_quinella_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((odds_url + horse_number_1 + horse_number_2).encode()).hexdigest()

        logger.debug(f"#process_odds_quinella_item: delete: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("delete from odds_quinella where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_quinella_item: insert: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("""insert into odds_quinella (
                id,
                odds_url,
                horse_number_1,
                horse_number_2,
                odds
            ) values (
                %s, %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            horse_number_1,
            horse_number_2,
            item["odds"][0] if "odds" in item else None,
        ))

        self.db_conn.commit()

    def process_odds_exacta_item(self, item, spider):
        logger.info(f"#process_odds_exacta_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((odds_url + horse_number_1 + horse_number_2).encode()).hexdigest()

        logger.debug(f"#process_odds_exacta_item: delete: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("delete from odds_exacta where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_exacta_item: insert: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("""insert into odds_exacta (
                id,
                odds_url,
                horse_number_1,
                horse_number_2,
                odds
            ) values (
                %s, %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            horse_number_1,
            horse_number_2,
            item["odds"][0] if "odds" in item else None,
        ))

        self.db_conn.commit()

    def process_odds_quinella_place_item(self, item, spider):
        logger.info(f"#process_odds_quinella_place_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((odds_url + horse_number_1 + horse_number_2).encode()).hexdigest()

        logger.debug(f"#process_odds_quinella_place_item: delete: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("delete from odds_quinella_place where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_quinella_place_item: insert: id={id}, odds_url={odds_url}, horse_number_1={horse_number_1}, horse_number_2={horse_number_2}")

        self.db_cursor.execute("""insert into odds_quinella_place (
                id,
                odds_url,
                horse_number_1,
                horse_number_2,
                odds_lower,
                odds_upper
            ) values (
                %s, %s, %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            horse_number_1,
            horse_number_2,
            item["odds_lower"][0] if "odds_lower" in item else None,
            item["odds_upper"][0] if "odds_upper" in item else None,
        ))

        self.db_conn.commit()

    def process_odds_trio_item(self, item, spider):
        logger.info(f"#process_odds_trio_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_number_1_2 = item["horse_number_1_2"][0]
        horse_number_3 = item["horse_number_3"][0]
        id = hashlib.sha256((odds_url + horse_number_1_2 + horse_number_3).encode()).hexdigest()

        logger.debug(f"#process_odds_trio_item: delete: id={id}, odds_url={odds_url}, horse_number_1_2={horse_number_1_2}, horse_number_3={horse_number_3}")

        self.db_cursor.execute("delete from odds_trio where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_trio_item: insert: id={id}, odds_url={odds_url}, horse_number_1_2={horse_number_1_2}, horse_number_3={horse_number_3}")

        self.db_cursor.execute("""insert into odds_trio (
                id,
                odds_url,
                horse_number_1_2,
                horse_number_3,
                odds
            ) values (
                %s, %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            horse_number_1_2,
            horse_number_3,
            item["odds"][0] if "odds" in item else None,
        ))

        self.db_conn.commit()

    def process_odds_trifecta_item(self, item, spider):
        logger.info(f"#process_odds_trifecta_item: start: item={item}")

        # Delete db
        odds_url = item["odds_url"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((odds_url + horse_number).encode()).hexdigest()

        logger.debug(f"#process_odds_trifecta_item: delete: id={id}, odds_url={odds_url}, horse_number={horse_number}")

        self.db_cursor.execute("delete from odds_trifecta where id=%s",
                               (id,))

        # Insert db
        logger.debug(f"#process_odds_trifecta_item: insert: id={id}, odds_url={odds_url}, horse_number={horse_number}")

        self.db_cursor.execute("""insert into odds_trifecta (
                id,
                odds_url,
                horse_number,
                odds
            ) values (
                %s, %s, %s, %s
            )""", (
            id,
            odds_url,
            horse_number,
            item["odds"][0] if "odds" in item else None,
        ))

        self.db_conn.commit()
