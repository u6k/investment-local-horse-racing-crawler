from datetime import datetime
import os

from scrapy.crawler import Crawler

from investment_local_horse_racing_crawler.spiders.local_horse_racing_spider import LocalHorseRacingSpider
from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem
from investment_local_horse_racing_crawler.pipelines import PostgreSQLPipeline


class TestPostgreSQLPipeline:
    def setup(self):
        # Setting pipeline
        settings = {
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT"),
            "DB_DATABASE": os.getenv("DB_DATABASE"),
            "DB_USERNAME": os.getenv("DB_USERNAME"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        }
        crawler = Crawler(LocalHorseRacingSpider, settings)
        self.pipeline = PostgreSQLPipeline.from_crawler(crawler)
        self.pipeline.open_spider(None)

        # Setting db
        self.pipeline.db_cursor.execute("delete from race_info")
        self.pipeline.db_cursor.execute("delete from race_denma")

    def teardown(self):
        self.pipeline.close_spider(None)

    def test_process_race_info_item(self):
        # Setup
        item = RaceInfoItem()
        item['added_money'] = ['\n'
                               '\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t賞金\xa01着\xa0150,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t2着\xa042,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t3着\xa021,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t4着\xa012,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t5着\xa07,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\n'
                               '\t\t']
        item['course_type_length'] = ['ダ200m']
        item['moisture'] = ['2.6%']
        item['place_name'] = ['帯広:第1競走']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['race_name'] = ['\n\t\t\tＣ１－１\n\t\t']
        item['race_round'] = ['R1']
        item['start_date'] = ['2020年3月1日(日)']
        item['start_time'] = ['発走時間 13:00']
        item['weather'] = ['/local/images/ico-tenki-6.gif?20180131184058']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['race_round'] == 1
        assert new_item["start_datetime"] == datetime(2020, 3, 1, 13, 0, 0)
        assert new_item['place_name'] == '帯広:第1競走'
        assert new_item['race_name'] == 'Ｃ１－１'
        assert new_item['course_type'] == 'ダ'
        assert new_item['course_length'] == 200
        assert new_item['weather'] == "雪"
        assert new_item['moisture'] == 2.6
        assert new_item['added_money'] == '賞金\xa01着\xa0150,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t2着\xa042,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t3着\xa021,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t4着\xa012,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t5着\xa07,000円'

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info")

        race_infos = self.pipeline.db_cursor.fetchall()
        assert len(race_infos) == 1

        race_info = race_infos[0]
        assert race_info['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_info['race_round'] == 1
        assert race_info["start_datetime"] == datetime(2020, 3, 1, 13, 0, 0)
        assert race_info['place_name'] == '帯広:第1競走'
        assert race_info['race_name'] == 'Ｃ１－１'
        assert race_info['course_type'] == 'ダ'
        assert race_info['course_length'] == 200
        assert race_info['weather'] == "雪"
        assert race_info['moisture'] == 2.6
        assert race_info['added_money'] == '賞金\xa01着\xa0150,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t2着\xa042,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t3着\xa021,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t4着\xa012,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t5着\xa07,000円'

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_info")

        race_infos = self.pipeline.db_cursor.fetchall()
        assert len(race_infos) == 1

    def test_process_race_denma_item_1(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t\t\t',
                            '\n\t\t\t\t\t',
                            '\n\t\t\t\t\t(3人気)\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280190375']
        item['horse_number'] = ['1']
        item['horse_weight'] = ['\n\t\t\t\t1042']
        item['horse_weight_diff'] = ['\n\t\t\t\t-7\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=038071']
        item['jockey_weight'] = ['660']
        item['odds_win'] = ['\n\t\t\t\t\t\t5.5\n\t\t\t\t\t']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=018052']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['bracket_number'] == 1
        assert new_item['horse_number'] == 1
        assert new_item['horse_id'] == '2280190375'
        assert new_item['horse_weight'] == 1042
        assert new_item['horse_weight_diff'] == -7
        assert new_item['trainer_id'] == '018052'
        assert new_item['jockey_id'] == '038071'
        assert new_item['jockey_weight'] == 660
        assert new_item['odds_win'] == 5.5
        assert new_item['favorite'] == 3

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_denma['bracket_number'] == 1
        assert race_denma['horse_number'] == 1
        assert race_denma['horse_id'] == '2280190375'
        assert race_denma['horse_weight'] == 1042
        assert race_denma['horse_weight_diff'] == -7
        assert race_denma['trainer_id'] == '018052'
        assert race_denma['jockey_id'] == '038071'
        assert race_denma['jockey_weight'] == 660
        assert race_denma['odds_win'] == 5.5
        assert race_denma['favorite'] == 3

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

    def test_process_race_denma_item_2(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t8\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t\t\t',
                            '\n\t\t\t\t\t',
                            '\n\t\t\t\t\t(1人気)\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280190252']
        item['horse_number'] = ['9']
        item['horse_weight'] = ['\n\t\t\t\t1092']
        item['horse_weight_diff'] = ['\n\t\t\t\t+12\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=038052']
        item['jockey_weight'] = ['650']
        item['odds_win'] = ['\n\t\t\t\t\t\t2.8\n\t\t\t\t\t']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=018077']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['bracket_number'] == 8
        assert new_item['horse_number'] == 9
        assert new_item['horse_id'] == '2280190252'
        assert new_item['horse_weight'] == 1092
        assert new_item['horse_weight_diff'] == 12
        assert new_item['trainer_id'] == '018077'
        assert new_item['jockey_id'] == '038052'
        assert new_item['jockey_weight'] == 650
        assert new_item['odds_win'] == 2.8
        assert new_item['favorite'] == 1

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_denma['bracket_number'] == 8
        assert race_denma['horse_number'] == 9
        assert race_denma['horse_id'] == '2280190252'
        assert race_denma['horse_weight'] == 1092
        assert race_denma['horse_weight_diff'] == 12
        assert race_denma['trainer_id'] == '018077'
        assert race_denma['jockey_id'] == '038052'
        assert race_denma['jockey_weight'] == 650
        assert race_denma['odds_win'] == 2.8
        assert race_denma['favorite'] == 1

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1
