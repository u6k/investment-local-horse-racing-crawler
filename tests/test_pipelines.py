from datetime import datetime
import os

from scrapy.crawler import Crawler

from investment_local_horse_racing_crawler.spiders.local_horse_racing_spider import LocalHorseRacingSpider
from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem, OddsWinPlaceItem, RaceResultItem, RacePayoffItem
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
