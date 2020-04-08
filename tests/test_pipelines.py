from datetime import datetime
import os

from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from investment_local_horse_racing_crawler.spiders.local_horse_racing_spider import LocalHorseRacingSpider
from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem, OddsWinPlaceItem, RaceResultItem, RacePayoffItem, HorseItem, JockeyItem, TrainerItem
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
        self.pipeline.db_cursor.execute("delete from odds_win")
        self.pipeline.db_cursor.execute("delete from odds_place")
        self.pipeline.db_cursor.execute("delete from race_result")
        self.pipeline.db_cursor.execute("delete from race_payoff")
        self.pipeline.db_cursor.execute("delete from horse")
        self.pipeline.db_cursor.execute("delete from jockey")
        self.pipeline.db_cursor.execute("delete from trainer")

    def teardown(self):
        self.pipeline.close_spider(None)

    def test_process_race_info_item_1(self):
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

    def test_process_race_info_item_2(self):
        # Setup
        item = RaceInfoItem()
        item['added_money'] = ['\n'
                               '\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t賞金\xa01着\xa02,500,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t2着\xa0750,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t3着\xa0250,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t4着\xa0150,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\t\t\n'
                               '\t\t\t\t\t5着\xa0100,000円\n'
                               '\t\t\t\t\n'
                               '\t\t\t\n'
                               '\t\t\n'
                               '\t\t']
        item['course_type_length'] = ['ダ1400m']
        item['place_name'] = ['佐賀:第11競走']
        item['race_id'] = ['sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=11']
        item['race_name'] = ['\n\t\t\tウインターチャンピオンオープン\n\t\t']
        item['race_round'] = ['R11']
        item['start_date'] = ['2020年1月26日(日)']
        item['start_time'] = ['発走時間 18:10']
        item['weather'] = ['/local/images/ico-tenki-2.gif?20180131184058']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=11'
        assert new_item['race_round'] == 11
        assert new_item['start_datetime'] == datetime(2020, 1, 26, 18, 10, 0)
        assert new_item['place_name'] == '佐賀:第11競走'
        assert new_item['race_name'] == 'ウインターチャンピオンオープン'
        assert new_item['course_type'] == 'ダ'
        assert new_item['course_length'] == 1400
        assert new_item['weather'] == 'くもり'
        assert new_item['moisture'] is None
        assert new_item['added_money'] == '賞金\xa01着\xa02,500,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t2着\xa0750,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t3着\xa0250,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t4着\xa0150,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t5着\xa0100,000円'

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info")

        race_infos = self.pipeline.db_cursor.fetchall()
        assert len(race_infos) == 1

        race_info = race_infos[0]
        assert race_info['race_id'] == 'sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=11'
        assert race_info['race_round'] == 11
        assert race_info['start_datetime'] == datetime(2020, 1, 26, 18, 10, 0)
        assert race_info['place_name'] == '佐賀:第11競走'
        assert race_info['race_name'] == 'ウインターチャンピオンオープン'
        assert race_info['course_type'] == 'ダ'
        assert race_info['course_length'] == 1400
        assert race_info['weather'] == 'くもり'
        assert race_info['moisture'] is None
        assert race_info['added_money'] == '賞金\xa01着\xa02,500,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t2着\xa0750,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t3着\xa0250,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t4着\xa0150,000円\n\t\t\t\t\n\t\t\t\n\t\t\t\t\n\t\t\t\t\t5着\xa0100,000円'

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
        assert new_item['race_denma_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190252'
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
        assert race_denma['race_denma_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190252'
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

    def test_process_race_denma_item_3(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t\t\t',
                            '\n\t\t\t\t\t',
                            '\n\t\t\t\t\t(8人気)\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2014100939']
        item['horse_number'] = ['1']
        item['horse_weight'] = ['\n\t\t\t\t478']
        item['horse_weight_diff'] = ['\n\t\t\t\t±0\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=030573']
        item['jockey_weight'] = ['54.0']
        item['odds_win'] = ['\n\t\t\t\t\t\t51.7\n\t\t\t\t\t']
        item['race_id'] = ['sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=9']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=010969']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=9'
        assert new_item['bracket_number'] == 1
        assert new_item['horse_number'] == 1
        assert new_item['horse_id'] == '2014100939'
        assert new_item['horse_weight'] == 478
        assert new_item['horse_weight_diff'] == 0
        assert new_item['trainer_id'] == '010969'
        assert new_item['jockey_id'] == '030573'
        assert new_item['jockey_weight'] == 54.0
        assert new_item['odds_win'] == 51.7
        assert new_item['favorite'] == 8

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=30&raceDy=20200126&opTrackCd=61&raceNb=9'
        assert race_denma['bracket_number'] == 1
        assert race_denma['horse_number'] == 1
        assert race_denma['horse_id'] == '2014100939'
        assert race_denma['horse_weight'] == 478
        assert race_denma['horse_weight_diff'] == 0
        assert race_denma['trainer_id'] == '010969'
        assert race_denma['jockey_id'] == '030573'
        assert race_denma['jockey_weight'] == 54.0
        assert race_denma['odds_win'] == 51.7
        assert race_denma['favorite'] == 8

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

    def test_process_race_denma_item_4(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t\t\t',
                            '\n\t\t\t\t\t',
                            '\n\t\t\t\t\t(12人気)\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2014103054']
        item['horse_number'] = ['1']
        item['horse_weight'] = ['\n\t\t\t\t517']
        item['horse_weight_diff'] = ['\n\t\t\t\t-1\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=031286']
        item['jockey_weight'] = ['▲53.0']
        item['odds_win'] = ['\n\t\t\t\t\t\t43.1\n\t\t\t\t\t']
        item['race_id'] = ['sponsorCd=29&raceDy=20200126&opTrackCd=55&raceNb=11']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=011445']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=29&raceDy=20200126&opTrackCd=55&raceNb=11'
        assert new_item['bracket_number'] == 1
        assert new_item['horse_number'] == 1
        assert new_item['horse_id'] == '2014103054'
        assert new_item['horse_weight'] == 517
        assert new_item['horse_weight_diff'] == -1
        assert new_item['trainer_id'] == '011445'
        assert new_item['jockey_id'] == '031286'
        assert new_item['jockey_weight'] == 53.0
        assert new_item['odds_win'] == 43.1
        assert new_item['favorite'] == 12

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=29&raceDy=20200126&opTrackCd=55&raceNb=11'
        assert race_denma['bracket_number'] == 1
        assert race_denma['horse_number'] == 1
        assert race_denma['horse_id'] == '2014103054'
        assert race_denma['horse_weight'] == 517
        assert race_denma['horse_weight_diff'] == -1
        assert race_denma['trainer_id'] == '011445'
        assert race_denma['jockey_id'] == '031286'
        assert race_denma['jockey_weight'] == 53.0
        assert race_denma['odds_win'] == 43.1
        assert race_denma['favorite'] == 12

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

    def test_process_race_denma_item_5(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2014105259']
        item['horse_number'] = ['1']
        item['horse_weight'] = ['\n\t\t\t\t462']
        item['horse_weight_diff'] = ['\n\t\t\t\t-9\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=031161']
        item['jockey_weight'] = ['54.0']
        item['race_id'] = ['sponsorCd=30&raceDy=20200105&opTrackCd=61&raceNb=10']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=010845']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=30&raceDy=20200105&opTrackCd=61&raceNb=10'
        assert new_item['bracket_number'] == 1
        assert new_item['horse_number'] == 1
        assert new_item['horse_id'] == '2014105259'
        assert new_item['horse_weight'] == 462
        assert new_item['horse_weight_diff'] == -9
        assert new_item['trainer_id'] == '010845'
        assert new_item['jockey_id'] == '031161'
        assert new_item['jockey_weight'] == 54.0
        assert new_item['odds_win'] is None
        assert new_item['favorite'] is None

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=30&raceDy=20200105&opTrackCd=61&raceNb=10'
        assert race_denma['bracket_number'] == 1
        assert race_denma['horse_number'] == 1
        assert race_denma['horse_id'] == '2014105259'
        assert race_denma['horse_weight'] == 462
        assert race_denma['horse_weight_diff'] == -9
        assert race_denma['trainer_id'] == '010845'
        assert race_denma['jockey_id'] == '031161'
        assert race_denma['jockey_weight'] == 54.0
        assert race_denma['odds_win'] is None
        assert race_denma['favorite'] is None

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

    def test_process_race_denma_item_6(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['\n\t\t\t\t\t3\n\t\t\t\t']
        item['favorite'] = ['\n\t\t\t\t\n\t\t\t']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2013106207']
        item['horse_number'] = ['3']
        item['horse_weight'] = ['\n\t\t\t\t']
        item['horse_weight_diff'] = ['\n\t\t\t\t\n\t\t\t']
        item['jockey_id'] = ['/keiba/JockeyDetail.do?jkyNb=030600']
        item['jockey_weight'] = ['56.0']
        item['race_id'] = ['sponsorCd=29&raceDy=20200113&opTrackCd=55&raceNb=1']
        item['trainer_id'] = ['/keiba/TrainerDetail.do?trainerNb=010913']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_id'] == 'sponsorCd=29&raceDy=20200113&opTrackCd=55&raceNb=1'
        assert new_item['bracket_number'] == 3
        assert new_item['horse_number'] == 3
        assert new_item['horse_id'] == '2013106207'
        assert new_item['horse_weight'] is None
        assert new_item['horse_weight_diff'] is None
        assert new_item['trainer_id'] == '010913'
        assert new_item['jockey_id'] == '030600'
        assert new_item['jockey_weight'] == 56.0
        assert new_item['odds_win'] is None
        assert new_item['favorite'] is None

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

        race_denma = race_denmas[0]
        assert race_denma['race_id'] == 'sponsorCd=29&raceDy=20200113&opTrackCd=55&raceNb=1'
        assert race_denma['bracket_number'] == 3
        assert race_denma['horse_number'] == 3
        assert race_denma['horse_id'] == '2013106207'
        assert race_denma['horse_weight'] is None
        assert race_denma['horse_weight_diff'] is None
        assert race_denma['trainer_id'] == '010913'
        assert race_denma['jockey_id'] == '030600'
        assert race_denma['jockey_weight'] == 56.0
        assert race_denma['odds_win'] is None
        assert race_denma['favorite'] is None

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        race_denmas = self.pipeline.db_cursor.fetchall()
        assert len(race_denmas) == 1

    def test_process_odds_win_place_item_1(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280190375']
        item['horse_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['odds_place_max'] = ['1.2']
        item['odds_place_min'] = ['1.0']
        item['odds_win'] = ['5.5']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_win")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        self.pipeline.db_cursor.execute("select * from odds_place")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['odds_win_place_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190375'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['horse_number'] == 1
        assert new_item['horse_id'] == '2280190375'
        assert new_item['odds_win'] == 5.5
        assert new_item['odds_place_max'] == 1.2
        assert new_item['odds_place_min'] == 1.0

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        odds_win = odds_wins[0]
        assert odds_win['odds_win_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190375'
        assert odds_win['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert odds_win['horse_number'] == 1
        assert odds_win['horse_id'] == '2280190375'
        assert odds_win['odds_win'] == 5.5

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 1

        odds_place = odds_places[0]
        assert odds_place['odds_place_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190375'
        assert odds_place['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert odds_place['horse_number'] == 1
        assert odds_place['horse_id'] == '2280190375'
        assert odds_place['odds_place_max'] == 1.2
        assert odds_place['odds_place_min'] == 1.0

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 1

    def test_process_odds_win_place_item_2(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280190252']
        item['horse_number'] = ['\n\t\t\t\t\t9\n\t\t\t\t']
        item['odds_place_max'] = ['2.0']
        item['odds_place_min'] = ['1.2']
        item['odds_win'] = ['2.8']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_win")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        self.pipeline.db_cursor.execute("select * from odds_place")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['odds_win_place_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190252'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['horse_number'] == 9
        assert new_item['horse_id'] == '2280190252'
        assert new_item['odds_win'] == 2.8
        assert new_item['odds_place_max'] == 2.0
        assert new_item['odds_place_min'] == 1.2

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        odds_win = odds_wins[0]
        assert odds_win['odds_win_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190252'
        assert odds_win['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert odds_win['horse_number'] == 9
        assert odds_win['horse_id'] == '2280190252'
        assert odds_win['odds_win'] == 2.8

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 1

        odds_place = odds_places[0]
        assert odds_place['odds_place_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190252'
        assert odds_place['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert odds_place['horse_number'] == 9
        assert odds_place['horse_id'] == '2280190252'
        assert odds_place['odds_place_max'] == 2.0
        assert odds_place['odds_place_min'] == 1.2

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 1

    def test_process_odds_win_place_item_3(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2013101003']
        item['horse_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['race_id'] = ['sponsorCd=26&raceDy=20200102&opTrackCd=51&raceNb=12']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_win")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        self.pipeline.db_cursor.execute("select * from odds_place")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        try:
            self.pipeline.process_item(item, None)
            assert False
        except DropItem as e:
            assert e.__str__() == "オッズなし"

        # After check
        self.pipeline.db_cursor.execute("select * from odds_win")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        self.pipeline.db_cursor.execute("select * from odds_place")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

    def test_process_odds_win_place_item_4(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2230191476']
        item['horse_number'] = ['\n\t\t\t\t\t1\n\t\t\t\t']
        item['odds_win'] = ['4.2']
        item['race_id'] = ['sponsorCd=04&raceDy=20191226&opTrackCd=03&raceNb=11']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_win")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        self.pipeline.db_cursor.execute("select * from odds_place")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['odds_win_place_id'] == 'sponsorCd=04&raceDy=20191226&opTrackCd=03&raceNb=11_2230191476'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20191226&opTrackCd=03&raceNb=11'
        assert new_item['horse_id'] == '2230191476'
        assert new_item['horse_number'] == 1
        assert new_item['odds_win'] == 4.2
        assert new_item['odds_place_max'] is None
        assert new_item['odds_place_min'] is None

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        odds_win = odds_wins[0]
        assert odds_win['odds_win_id'] == 'sponsorCd=04&raceDy=20191226&opTrackCd=03&raceNb=11_2230191476'
        assert odds_win['race_id'] == 'sponsorCd=04&raceDy=20191226&opTrackCd=03&raceNb=11'
        assert odds_win['horse_id'] == '2230191476'
        assert odds_win['horse_number'] == 1
        assert odds_win['odds_win'] == 4.2

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 0

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_win")

        odds_wins = self.pipeline.db_cursor.fetchall()
        assert len(odds_wins) == 1

        self.pipeline.db_cursor.execute("select * from odds_place")

        odds_places = self.pipeline.db_cursor.fetchall()
        assert len(odds_places) == 0

    def test_process_race_result_item_1(self):
        # Setup
        item = RaceResultItem()
        item['arrival_time'] = ['1:51.6']
        item['bracket_number'] = ['6']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280190029']
        item['horse_number'] = ['6']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['result'] = ['1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_result")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_result_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190029'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['bracket_number'] == 6
        assert new_item['horse_number'] == 6
        assert new_item['horse_id'] == '2280190029'
        assert new_item['result'] == 1
        assert new_item['arrival_time'] == 111.6

        # Check db
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

        race_result = race_results[0]
        assert race_result['race_result_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280190029'
        assert race_result['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_result['bracket_number'] == 6
        assert race_result['horse_number'] == 6
        assert race_result['horse_id'] == '2280190029'
        assert race_result['result'] == 1
        assert race_result['arrival_time'] == 111.6

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

    def test_process_race_result_item_2(self):
        # Setup
        item = RaceResultItem()
        item['arrival_time'] = ['2:06.7']
        item['bracket_number'] = ['8']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2280191034']
        item['horse_number'] = ['8']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['result'] = ['9']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_result")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_result_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280191034'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['bracket_number'] == 8
        assert new_item['horse_number'] == 8
        assert new_item['horse_id'] == '2280191034'
        assert new_item['result'] == 9
        assert new_item['arrival_time'] == 126.7

        # Check db
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

        race_result = race_results[0]
        assert race_result['race_result_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_2280191034'
        assert race_result['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_result['bracket_number'] == 8
        assert race_result['horse_number'] == 8
        assert race_result['horse_id'] == '2280191034'
        assert race_result['result'] == 9
        assert race_result['arrival_time'] == 126.7

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

    def test_process_race_result_item_3(self):
        # Setup
        item = RaceResultItem()
        item['bracket_number'] = ['7']
        item['horse_id'] = ['/keiba/HorseDetail.do?lineageNb=2017101608']
        item['horse_number'] = ['10']
        item['race_id'] = ['sponsorCd=30&raceDy=20200104&opTrackCd=61&raceNb=9']
        item['result'] = ['-']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_result")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_result_id'] == 'sponsorCd=30&raceDy=20200104&opTrackCd=61&raceNb=9_2017101608'
        assert new_item['race_id'] == 'sponsorCd=30&raceDy=20200104&opTrackCd=61&raceNb=9'
        assert new_item['bracket_number'] == 7
        assert new_item['horse_number'] == 10
        assert new_item['horse_id'] == '2017101608'
        assert new_item['result'] is None
        assert new_item['arrival_time'] is None

        # Check db
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

        race_result = race_results[0]
        assert race_result['race_result_id'] == 'sponsorCd=30&raceDy=20200104&opTrackCd=61&raceNb=9_2017101608'
        assert race_result['race_id'] == 'sponsorCd=30&raceDy=20200104&opTrackCd=61&raceNb=9'
        assert race_result['bracket_number'] == 7
        assert race_result['horse_number'] == 10
        assert race_result['horse_id'] == '2017101608'
        assert race_result['result'] is None
        assert race_result['arrival_time'] is None

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_result")

        race_results = self.pipeline.db_cursor.fetchall()
        assert len(race_results) == 1

    def test_process_race_payoff_item_1(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['6番人気']
        item['horse_number'] = ['6']
        item['odds'] = ['1,250円']
        item['payoff_type'] = ['単勝']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_win_6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'win'
        assert new_item['horse_number_1'] == 6
        assert new_item['horse_number_2'] is None
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 12.5
        assert new_item['favorite'] == 6

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_win_6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'win'
        assert race_payoff['horse_number_1'] == 6
        assert race_payoff['horse_number_2'] is None
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 12.5
        assert race_payoff['favorite'] == 6

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_2(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['7番人気']
        item['horse_number'] = ['6']
        item['odds'] = ['470円']
        item['payoff_type'] = ['複勝']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_place_6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'place'
        assert new_item['horse_number_1'] == 6
        assert new_item['horse_number_2'] is None
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 4.7
        assert new_item['favorite'] == 7

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_place_6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'place'
        assert race_payoff['horse_number_1'] == 6
        assert race_payoff['horse_number_2'] is None
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 4.7
        assert race_payoff['favorite'] == 7

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_3(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['18番人気']
        item['horse_number'] = ['4-6']
        item['odds'] = ['4,690円']
        item['payoff_type'] = ['枠連']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_bracket_quinella_4-6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'bracket_quinella'
        assert new_item['horse_number_1'] == 4
        assert new_item['horse_number_2'] == 6
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 46.9
        assert new_item['favorite'] == 18

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_bracket_quinella_4-6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'bracket_quinella'
        assert race_payoff['horse_number_1'] == 4
        assert race_payoff['horse_number_2'] == 6
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 46.9
        assert race_payoff['favorite'] == 18

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_4(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['18番人気']
        item['horse_number'] = ['4-6']
        item['odds'] = ['3,930円']
        item['payoff_type'] = ['馬連']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_quinella_4-6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'quinella'
        assert new_item['horse_number_1'] == 4
        assert new_item['horse_number_2'] == 6
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 39.3
        assert new_item['favorite'] == 18

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_quinella_4-6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'quinella'
        assert race_payoff['horse_number_1'] == 4
        assert race_payoff['horse_number_2'] == 6
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 39.3
        assert race_payoff['favorite'] == 18

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_5(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['18番人気']
        item['horse_number'] = ['6-4']
        item['odds'] = ['4,470円']
        item['payoff_type'] = ['馬単']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_exacta_6-4'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'exacta'
        assert new_item['horse_number_1'] == 6
        assert new_item['horse_number_2'] == 4
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 44.7
        assert new_item['favorite'] == 18

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_exacta_6-4'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'exacta'
        assert race_payoff['horse_number_1'] == 6
        assert race_payoff['horse_number_2'] == 4
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 44.7
        assert race_payoff['favorite'] == 18

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_6(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['18番人気']
        item['horse_number'] = ['4-6']
        item['odds'] = ['1,060円']
        item['payoff_type'] = ['ワイド']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_quinella_place_4-6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'quinella_place'
        assert new_item['horse_number_1'] == 4
        assert new_item['horse_number_2'] == 6
        assert new_item['horse_number_3'] is None
        assert new_item['odds'] == 10.6
        assert new_item['favorite'] == 18

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_quinella_place_4-6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'quinella_place'
        assert race_payoff['horse_number_1'] == 4
        assert race_payoff['horse_number_2'] == 6
        assert race_payoff['horse_number_3'] is None
        assert race_payoff['odds'] == 10.6
        assert race_payoff['favorite'] == 18

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_7(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['19番人気']
        item['horse_number'] = ['2-4-6']
        item['odds'] = ['3,890円']
        item['payoff_type'] = ['3連複']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_trio_2-4-6'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'trio'
        assert new_item['horse_number_1'] == 2
        assert new_item['horse_number_2'] == 4
        assert new_item['horse_number_3'] == 6
        assert new_item['odds'] == 38.9
        assert new_item['favorite'] == 19

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_trio_2-4-6'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'trio'
        assert race_payoff['horse_number_1'] == 2
        assert race_payoff['horse_number_2'] == 4
        assert race_payoff['horse_number_3'] == 6
        assert race_payoff['odds'] == 38.9
        assert race_payoff['favorite'] == 19

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_8(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['87番人気']
        item['horse_number'] = ['6-4-2']
        item['odds'] = ['20,460円']
        item['payoff_type'] = ['3連単']
        item['race_id'] = ['sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_trifecta_6-4-2'
        assert new_item['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert new_item['payoff_type'] == 'trifecta'
        assert new_item['horse_number_1'] == 6
        assert new_item['horse_number_2'] == 4
        assert new_item['horse_number_3'] == 2
        assert new_item['odds'] == 204.6
        assert new_item['favorite'] == 87

        # Check db
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

        race_payoff = race_payoffs[0]
        assert race_payoff['race_payoff_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1_trifecta_6-4-2'
        assert race_payoff['race_id'] == 'sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1'
        assert race_payoff['payoff_type'] == 'trifecta'
        assert race_payoff['horse_number_1'] == 6
        assert race_payoff['horse_number_2'] == 4
        assert race_payoff['horse_number_3'] == 2
        assert race_payoff['odds'] == 204.6
        assert race_payoff['favorite'] == 87

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_payoff")

        race_payoffs = self.pipeline.db_cursor.fetchall()
        assert len(race_payoffs) == 1

    def test_process_race_payoff_item_9(self):
        # Setup
        item = RacePayoffItem()
        item['horse_number'] = ['発売なし']
        item['payoff_type'] = ['枠連']
        item['race_id'] = ['sponsorCd=04&raceDy=20200302&opTrackCd=03&raceNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        try:
            self.pipeline.process_item(item, None)
            assert False
        except DropItem as e:
            assert e.__str__() == "発売なし"

        # After check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

    def test_process_race_payoff_item_10(self):
        # Setup
        item = RacePayoffItem()
        item['favorite'] = ['-']
        item['horse_number'] = ['-']
        item['odds'] = ['100円']
        item['payoff_type'] = ['単勝']
        item['race_id'] = ['sponsorCd=26&raceDy=20200108&opTrackCd=51&raceNb=9']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        try:
            self.pipeline.process_item(item, None)
            assert False
        except DropItem as e:
            assert e.__str__() == "取り止め"

        # After check
        self.pipeline.db_cursor.execute("select * from race_payoff")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

    def test_process_horse_item_1(self):
        # Setup
        item = HorseItem()
        item['birthday'] = ['2016年3月30日']
        item['breeder'] = ['橋\u3000本\u3000岩\u3000雄']
        item['breeding_farm'] = ['北海道日高郡新ひだか町']
        item['coat_color'] = ['栗毛']
        item['gender_age'] = ['牡｜4 歳']
        item['grand_parent_horse_name_1'] = ['ハイパワード\u200b']
        item['grand_parent_horse_name_2'] = ['スーパーマコト\u200b']
        item['grand_parent_horse_name_3'] = ['肖\u3000命\u200b']
        item['grand_parent_horse_name_4'] = ['宝\u3000秀\u200b']
        item['horse_id'] = ['lineageNb=2280190375']
        item['horse_name'] = ['\n\tミヤビホウリキ\xa0']
        item['owner'] = ['中島雅也']
        item['parent_horse_name_1'] = ['アサノカイリキ\u200b']
        item['parent_horse_name_2'] = ['千\u3000花\u200b']

        # Before check
        self.pipeline.db_cursor.execute("select * from horse")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['horse_id'] == '2280190375'
        assert new_item['horse_name'] == 'ミヤビホウリキ'
        assert new_item['gender'] == '牡'
        assert new_item['age'] == 4
        assert new_item['birthday'] == datetime(2016, 3, 30, 0, 0, 0)
        assert new_item['coat_color'] == '栗毛'
        assert new_item['owner'] == '中島雅也'
        assert new_item['breeder'] == '橋\u3000本\u3000岩\u3000雄'
        assert new_item['breeding_farm'] == '北海道日高郡新ひだか町'
        assert new_item['parent_horse_name_1'] == 'アサノカイリキ\u200b'
        assert new_item['parent_horse_name_2'] == '千\u3000花\u200b'
        assert new_item['grand_parent_horse_name_1'] == 'ハイパワード\u200b'
        assert new_item['grand_parent_horse_name_2'] == 'スーパーマコト\u200b'
        assert new_item['grand_parent_horse_name_3'] == '肖\u3000命\u200b'
        assert new_item['grand_parent_horse_name_4'] == '宝\u3000秀\u200b'

        # Check db
        self.pipeline.db_cursor.execute("select * from horse")

        horses = self.pipeline.db_cursor.fetchall()
        assert len(horses) == 1

        horse = horses[0]
        assert horse['horse_id'] == '2280190375'
        assert horse['horse_name'] == 'ミヤビホウリキ'
        assert horse['gender'] == '牡'
        assert horse['age'] == 4
        assert horse['birthday'] == datetime(2016, 3, 30, 0, 0, 0)
        assert horse['coat_color'] == '栗毛'
        assert horse['owner'] == '中島雅也'
        assert horse['breeder'] == '橋\u3000本\u3000岩\u3000雄'
        assert horse['breeding_farm'] == '北海道日高郡新ひだか町'
        assert horse['parent_horse_name_1'] == 'アサノカイリキ\u200b'
        assert horse['parent_horse_name_2'] == '千\u3000花\u200b'
        assert horse['grand_parent_horse_name_1'] == 'ハイパワード\u200b'
        assert horse['grand_parent_horse_name_2'] == 'スーパーマコト\u200b'
        assert horse['grand_parent_horse_name_3'] == '肖\u3000命\u200b'
        assert horse['grand_parent_horse_name_4'] == '宝\u3000秀\u200b'

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from horse")

        horses = self.pipeline.db_cursor.fetchall()
        assert len(horses) == 1

    def test_process_horse_item_2(self):
        # Setup
        item = HorseItem()
        item['birthday'] = ['1989年4月13日']
        item['breeder'] = ['谷川牧場']
        item['breeding_farm'] = ['北海道浦河郡浦河町']
        item['coat_color'] = ['鹿毛']
        item['gender_age'] = ['牡｜31 歳']
        item['grand_parent_horse_name_1'] = ['ステイールハート\u200b']
        item['grand_parent_horse_name_2'] = ['ニホンピロエバート\u200b']
        item['grand_parent_horse_name_3'] = ['シヤトーゲイ\u200b']
        item['grand_parent_horse_name_4'] = ['シンダイアンケー\u200b']
        item['horse_id'] = ['lineageNb=1989104729']
        item['horse_name'] = ['\n\tメモリーキャッチ\xa0']
        item['parent_horse_name_1'] = ['ニホンピロウイナー\u200b']
        item['parent_horse_name_2'] = ['ハシラベンダー\u200b']

        # Before check
        self.pipeline.db_cursor.execute("select * from horse")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['horse_id'] == '1989104729'
        assert new_item['horse_name'] == 'メモリーキャッチ'
        assert new_item['gender'] == '牡'
        assert new_item['age'] == 31
        assert new_item['birthday'] == datetime(1989, 4, 13, 0, 0, 0)
        assert new_item['coat_color'] == '鹿毛'
        assert new_item['owner'] is None
        assert new_item['breeder'] == '谷川牧場'
        assert new_item['breeding_farm'] == '北海道浦河郡浦河町'
        assert new_item['parent_horse_name_1'] == 'ニホンピロウイナー\u200b'
        assert new_item['parent_horse_name_2'] == 'ハシラベンダー\u200b'
        assert new_item['grand_parent_horse_name_1'] == 'ステイールハート\u200b'
        assert new_item['grand_parent_horse_name_2'] == 'ニホンピロエバート\u200b'
        assert new_item['grand_parent_horse_name_3'] == 'シヤトーゲイ\u200b'
        assert new_item['grand_parent_horse_name_4'] == 'シンダイアンケー\u200b'

        # Check db
        self.pipeline.db_cursor.execute("select * from horse")

        horses = self.pipeline.db_cursor.fetchall()
        assert len(horses) == 1

        horse = horses[0]
        assert horse['horse_id'] == '1989104729'
        assert horse['horse_name'] == 'メモリーキャッチ'
        assert horse['gender'] == '牡'
        assert horse['age'] == 31
        assert horse['birthday'] == datetime(1989, 4, 13, 0, 0, 0)
        assert horse['coat_color'] == '鹿毛'
        assert horse['owner'] is None
        assert horse['breeder'] == '谷川牧場'
        assert horse['breeding_farm'] == '北海道浦河郡浦河町'
        assert horse['parent_horse_name_1'] == 'ニホンピロウイナー\u200b'
        assert horse['parent_horse_name_2'] == 'ハシラベンダー\u200b'
        assert horse['grand_parent_horse_name_1'] == 'ステイールハート\u200b'
        assert horse['grand_parent_horse_name_2'] == 'ニホンピロエバート\u200b'
        assert horse['grand_parent_horse_name_3'] == 'シヤトーゲイ\u200b'
        assert horse['grand_parent_horse_name_4'] == 'シンダイアンケー\u200b'

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from horse")

        horses = self.pipeline.db_cursor.fetchall()
        assert len(horses) == 1

    def test_process_jockey_item(self):
        # Setup
        item = JockeyItem()
        item['belong_to'] = ['ばんえい']
        item['birthday'] = ['1983年9月23日']
        item['first_licensing_year'] = ['2007年']
        item['gender'] = ['男']
        item['jockey_id'] = ['jkyNb=038071']
        item['jockey_name'] = ['\n船\u3000山\u3000\u3000蔵\u3000人\xa0']

        # Before check
        self.pipeline.db_cursor.execute("select * from jockey")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['jockey_id'] == '038071'
        assert new_item['jockey_name'] == '船\u3000山\u3000\u3000蔵\u3000人'
        assert new_item['birthday'] == datetime(1983, 9, 23, 0, 0, 0)
        assert new_item['gender'] == '男'
        assert new_item['belong_to'] == 'ばんえい'
        assert new_item['first_licensing_year'] == 2007

        # Check db
        self.pipeline.db_cursor.execute("select * from jockey")

        jockeys = self.pipeline.db_cursor.fetchall()
        assert len(jockeys) == 1

        jockey = jockeys[0]
        assert jockey['jockey_id'] == '038071'
        assert jockey['jockey_name'] == '船\u3000山\u3000\u3000蔵\u3000人'
        assert jockey['birthday'] == datetime(1983, 9, 23, 0, 0, 0)
        assert jockey['gender'] == '男'
        assert jockey['belong_to'] == 'ばんえい'
        assert jockey['first_licensing_year'] == 2007

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from jockey")

        jockeys = self.pipeline.db_cursor.fetchall()
        assert len(jockeys) == 1

    def test_process_trainer_item(self):
        # Setup
        item = TrainerItem()
        item['belong_to'] = ['ばんえい']
        item['birthday'] = ['1959年1月2日']
        item['gender'] = ['男']
        item['trainer_id'] = ['trainerNb=018052']
        item['trainer_name'] = ['\n小\u3000林\u3000\u3000勝\u3000二\xa0']

        # Before check
        self.pipeline.db_cursor.execute("select * from trainer")
        assert len(self.pipeline.db_cursor.fetchall()) == 0

        # Execute
        new_item = self.pipeline.process_item(item, None)

        # Check return
        assert new_item['trainer_id'] == '018052'
        assert new_item['trainer_name'] == '小\u3000林\u3000\u3000勝\u3000二'
        assert new_item['birthday'] == datetime(1959, 1, 2, 0, 0, 0)
        assert new_item['gender'] == '男'
        assert new_item['belong_to'] == 'ばんえい'

        # Check db
        self.pipeline.db_cursor.execute("select * from trainer")

        trainers = self.pipeline.db_cursor.fetchall()
        assert len(trainers) == 1

        trainer = trainers[0]
        assert trainer['trainer_id'] == '018052'
        assert trainer['trainer_name'] == '小\u3000林\u3000\u3000勝\u3000二'
        assert trainer['birthday'] == datetime(1959, 1, 2, 0, 0, 0)
        assert trainer['gender'] == '男'
        assert trainer['belong_to'] == 'ばんえい'

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from trainer")

        trainers = self.pipeline.db_cursor.fetchall()
        assert len(trainers) == 1
