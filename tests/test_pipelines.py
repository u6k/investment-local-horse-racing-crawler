import logging
import os
from nose.tools import eq_, ok_

from scrapy.crawler import Crawler

from investment_local_horse_racing_crawler.scrapy.spiders.local_horse_racing_spider import LocalHorseRacingSpider
from investment_local_horse_racing_crawler.scrapy.items import CalendarItem, RaceInfoMiniItem, RaceInfoItem, RaceDenmaItem, RaceResultItem, RaceCornerPassingOrderItem, RaceRefundItem, HorseItem, JockeyItem, TrainerItem, OddsWinPlaceItem, OddsQuinellaItem, OddsExactaItem, OddsQuinellaPlaceItem, OddsTrioItem, OddsTrifectaItem
from investment_local_horse_racing_crawler.scrapy.pipelines import PostgreSQLPipeline


class TestPostgreSQLPipeline:
    def setup(self):
        logging.disable(logging.DEBUG)

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
        self.pipeline.db_cursor.execute("delete from calendar_race_url")
        self.pipeline.db_cursor.execute("delete from race_info_mini")
        self.pipeline.db_cursor.execute("delete from race_info")
        self.pipeline.db_cursor.execute("delete from race_denma")
        self.pipeline.db_cursor.execute("delete from race_result")
        self.pipeline.db_cursor.execute("delete from race_corner_passing_order")
        self.pipeline.db_cursor.execute("delete from race_refund")
        self.pipeline.db_cursor.execute("delete from horse")
        self.pipeline.db_cursor.execute("delete from jockey")
        self.pipeline.db_cursor.execute("delete from trainer")
        self.pipeline.db_cursor.execute("delete from odds_win_place")
        self.pipeline.db_cursor.execute("delete from odds_quinella")
        self.pipeline.db_cursor.execute("delete from odds_exacta")
        self.pipeline.db_cursor.execute("delete from odds_quinella_place")
        self.pipeline.db_cursor.execute("delete from odds_trio")
        self.pipeline.db_cursor.execute("delete from odds_trifecta")

    def teardown(self):
        self.pipeline.close_spider(None)

    def test_process_calendar_item(self):
        # Setup
        item = CalendarItem()
        item['calendar_url'] = ['https://www.oddspark.com/keiba/KaisaiCalendar.do?target=202004']
        item['race_list_urls'] = [
            '/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20200424&sponsorCd=04',
            '/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20200425&sponsorCd=04',
            '/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20200426&sponsorCd=04',
            '/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20200427&sponsorCd=04',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200415&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200416&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200422&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200423&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200428&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=06&raceDy=20200429&sponsorCd=01',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200405&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200406&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200407&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200412&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200413&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200414&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200419&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200420&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200421&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200426&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200427&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=12&raceDy=20200428&sponsorCd=06',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200405&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200407&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200413&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200414&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200419&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200421&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200428&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=41&raceDy=20200429&sponsorCd=18',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200401&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200402&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200403&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200406&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200414&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200415&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200416&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200417&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200428&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200429&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200430&sponsorCd=20',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200407&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200408&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200409&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200410&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200421&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200422&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200423&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=43&raceDy=20200424&sponsorCd=33',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200401&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200402&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200407&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200408&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200409&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200414&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200415&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200416&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200421&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200422&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200423&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200428&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200429&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=51&raceDy=20200430&sponsorCd=26',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200411&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200412&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200418&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200419&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200425&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=55&raceDy=20200426&sponsorCd=29',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200404&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200405&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200411&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200412&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200418&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200419&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200425&sponsorCd=30',
            '/keiba/OneDayRaceList.do?opTrackCd=61&raceDy=20200426&sponsorCd=30']

        # Before check
        self.pipeline.db_cursor.execute("select * from calendar_race_url")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from calendar_race_url")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 77)

        for record in records:
            eq_(len(record["id"]), 64)
            eq_(record["calendar_url"], "https://www.oddspark.com/keiba/KaisaiCalendar.do?target=202004")
            ok_(record["race_list_url"].startswith("/keiba/OneDayRaceList.do?"))

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from calendar_race_url")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 77)

    def test_process_race_info_mini_item_1(self):
        # Setup
        item = RaceInfoMiniItem()
        item['course_length'] = ['1R\xa0\xa0サラ系３歳１０組３歳１０ レース結果 ダ\xa0\xa01400m(右回り)\xa0\xa0発走時間\xa011:10']
        item['race_denma_url'] = ['/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20']
        item['race_list_url'] = ['https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200417&sponsorCd=20']
        item['race_name'] = ['1R\xa0\xa0サラ系３歳１０組３歳１０']
        item['start_time'] = ['11:10']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info_mini")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info_mini")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['course_length'], '1R\xa0\xa0サラ系３歳１０組３歳１０ レース結果 ダ\xa0\xa01400m(右回り)\xa0\xa0発走時間\xa011:10')
        eq_(record['race_denma_url'], '/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20')
        eq_(record['race_list_url'], 'https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200417&sponsorCd=20')
        eq_(record['race_name'], '1R\xa0\xa0サラ系３歳１０組３歳１０')
        eq_(record['start_time'], '11:10')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_info_mini")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_info_mini_item_2(self):
        # Setup
        item = RaceInfoMiniItem()
        item['course_length'] = ['11R\xa0\xa0狩勝賞オープン－１ ダ\xa0\xa0200m(直線)\xa0\xa0発走時間\xa020:10']
        item['race_denma_url'] = ['/keiba/RaceList.do?raceDy=20201019&opTrackCd=03&raceNb=11&sponsorCd=04']
        item['race_list_url'] = ['https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20201019&sponsorCd=04']
        item['race_name'] = ['11R\xa0\xa0狩勝賞オープン－１']
        item['start_time'] = ['20:10']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info_mini")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info_mini")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['course_length'], '11R\xa0\xa0狩勝賞オープン－１ ダ\xa0\xa0200m(直線)\xa0\xa0発走時間\xa020:10')
        eq_(record['race_denma_url'], '/keiba/RaceList.do?raceDy=20201019&opTrackCd=03&raceNb=11&sponsorCd=04')
        eq_(record['race_list_url'], 'https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=03&raceDy=20201019&sponsorCd=04')
        eq_(record['race_name'],  '11R\xa0\xa0狩勝賞オープン－１')
        eq_(record['start_time'], '20:10')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_info_mini")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_info_item_1(self):
        # Setup
        item = RaceInfoItem()
        item['course_type_length'] = ['ダ200m']
        item['moisture'] = ['1.8%']
        item['place_name'] = ['帯広:第1競走']
        item['prize_money'] = ['賞金\xa01着\xa0150,000円 2着\xa045,000円 3着\xa022,000円 4着\xa013,000円 5着\xa09,000円']
        item['race_denma_url'] = ['https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20201012&opTrackCd=03&raceNb=1']
        item['race_name'] = ['２歳Ｄ－７']
        item['race_round'] = ['R1']
        item['start_date'] = ['2020年10月12日(月)']
        item['start_time'] = ['発走時間 14:35']
        item['weather_url'] = ['/local/images/ico-tenki-4.gif?20180131184058']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['course_type_length'], 'ダ200m')
        eq_(record['moisture'], '1.8%')
        eq_(record['place_name'], '帯広:第1競走')
        eq_(record['prize_money'], '賞金\xa01着\xa0150,000円 2着\xa045,000円 3着\xa022,000円 4着\xa013,000円 5着\xa09,000円')
        eq_(record['race_denma_url'], 'https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20201012&opTrackCd=03&raceNb=1')
        eq_(record['race_name'], '２歳Ｄ－７')
        eq_(record['race_round'], 'R1')
        eq_(record['start_date'], '2020年10月12日(月)')
        eq_(record['start_time'], '発走時間 14:35')
        eq_(record['weather_url'], '/local/images/ico-tenki-4.gif?20180131184058')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_info")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_info_item_2(self):
        # Setup
        item = RaceInfoItem()
        item['course_condition'] = ['/local/images/ico-baba-1.gif?20180131184058']
        item['course_type_length'] = ['ダ1400m']
        item['place_name'] = ['笠松:第1競走']
        item['prize_money'] = ['賞金\xa01着\xa0290,000円 2着\xa067,000円 3着\xa029,000円 4着\xa021,000円 5着\xa015,000円']
        item['race_denma_url'] = ['https://www.oddspark.com/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20']
        item['race_name'] = ['サラ系３歳１０組３歳１０']
        item['race_round'] = ['R1']
        item['start_date'] = ['2020年4月17日(金)']
        item['start_time'] = ['発走時間 11:10']
        item['weather_url'] = ['/local/images/ico-tenki-2.gif?20180131184058']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_info")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_info")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['course_condition'], '/local/images/ico-baba-1.gif?20180131184058')
        eq_(record['course_type_length'], 'ダ1400m')
        eq_(record['place_name'], '笠松:第1競走')
        eq_(record['prize_money'], '賞金\xa01着\xa0290,000円 2着\xa067,000円 3着\xa029,000円 4着\xa021,000円 5着\xa015,000円')
        eq_(record['race_denma_url'], 'https://www.oddspark.com/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20')
        eq_(record['race_name'], 'サラ系３歳１０組３歳１０')
        eq_(record['race_round'], 'R1')
        eq_(record['start_date'], '2020年4月17日(金)')
        eq_(record['start_time'], '発走時間 11:10')
        eq_(record['weather_url'], '/local/images/ico-tenki-2.gif?20180131184058')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_info")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_denma_item_1(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['1']
        item['horse_number'] = ['1']
        item['horse_url'] = ['/keiba/HorseDetail.do?lineageNb=2300190102']
        item['horse_weight'] = ['965']
        item['horse_weight_diff'] = ['±0']
        item['jockey_url'] = ['/keiba/JockeyDetail.do?jkyNb=038054']
        item['jockey_weight'] = ['500']
        item['odds_win_favorite'] = ['2.2 (1人気)']
        item['race_denma_url'] = ['https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20201012&opTrackCd=03&raceNb=1']
        item['trainer_url'] = ['/keiba/TrainerDetail.do?trainerNb=018058']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['bracket_number'], '1')
        eq_(record['horse_number'], '1')
        eq_(record['horse_url'], '/keiba/HorseDetail.do?lineageNb=2300190102')
        eq_(record['horse_weight'], '965')
        eq_(record['horse_weight_diff'], '±0')
        eq_(record['jockey_url'], '/keiba/JockeyDetail.do?jkyNb=038054')
        eq_(record['jockey_weight'], '500')
        eq_(record['odds_win_favorite'], '2.2 (1人気)')
        eq_(record['race_denma_url'], 'https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20201012&opTrackCd=03&raceNb=1')
        eq_(record['trainer_url'], '/keiba/TrainerDetail.do?trainerNb=018058')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_denma_item_2(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['1']
        item['horse_number'] = ['1']
        item['horse_url'] = ['/keiba/HorseDetail.do?lineageNb=2017105139']
        item['horse_weight'] = ['535']
        item['horse_weight_diff'] = ['-2']
        item['jockey_url'] = ['/keiba/JockeyDetail.do?jkyNb=031101']
        item['jockey_weight'] = ['56.0']
        item['odds_win_favorite'] = ['47.8 (8人気)']
        item['race_denma_url'] = ['https://www.oddspark.com/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20']
        item['trainer_url'] = ['/keiba/TrainerDetail.do?trainerNb=010911']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_denma")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_denma")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['bracket_number'], '1')
        eq_(record['horse_number'], '1')
        eq_(record['horse_url'], '/keiba/HorseDetail.do?lineageNb=2017105139')
        eq_(record['horse_weight'], '535')
        eq_(record['horse_weight_diff'], '-2')
        eq_(record['jockey_url'], '/keiba/JockeyDetail.do?jkyNb=031101')
        eq_(record['jockey_weight'], '56.0')
        eq_(record['odds_win_favorite'], '47.8 (8人気)')
        eq_(record['race_denma_url'], 'https://www.oddspark.com/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20')
        eq_(record['trainer_url'], '/keiba/TrainerDetail.do?trainerNb=010911')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_denma")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_result_item_1(self):
        # Setup
        item = RaceResultItem()
        item['arrival_time'] = ['1:25.1']
        item['bracket_number'] = ['7']
        item['corner_passing_order'] = ['2-2-2-2']
        item['final_600_meters_time'] = ['40.2']
        item['horse_number'] = ['9']
        item['horse_url'] = ['/keiba/HorseDetail.do?lineageNb=2015101250']
        item['race_result_url'] = ['https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10']
        item['result'] = ['1']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_result")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_result")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['arrival_time'], '1:25.1')
        eq_(record['bracket_number'], '7')
        eq_(record['corner_passing_order'], '2-2-2-2')
        eq_(record['final_600_meters_time'], '40.2')
        eq_(record['horse_number'], '9')
        eq_(record['horse_url'], '/keiba/HorseDetail.do?lineageNb=2015101250')
        eq_(record['race_result_url'], 'https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10')
        eq_(record['result'], '1')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_result")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_corner_passing_order_item_1(self):
        # Setup
        item = RaceCornerPassingOrderItem()
        item['corner_number'] = ['１コーナー']
        item['passing_order'] = ['1, 9, 6, 12, 11, 7, 2, 5, 4, 8, 3, 10']
        item['race_result_url'] = ['https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_corner_passing_order")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_corner_passing_order")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['corner_number'], '１コーナー')
        eq_(record['passing_order'], '1, 9, 6, 12, 11, 7, 2, 5, 4, 8, 3, 10')
        eq_(record['race_result_url'], 'https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_corner_passing_order")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_race_refund_item_1(self):
        # Setup
        item = RaceRefundItem()
        item['betting_type'] = ['複勝']
        item['favorite'] = ['11番人気']
        item['horse_number'] = ['9']
        item['race_result_url'] = ['https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10']
        item['refund_money'] = ['520円']

        # Before check
        self.pipeline.db_cursor.execute("select * from race_refund")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from race_refund")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['betting_type'], '複勝')
        eq_(record['favorite'], '11番人気')
        eq_(record['horse_number'], '9')
        eq_(record['race_result_url'], 'https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10')
        eq_(record['refund_money'], '520円')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from race_refund")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

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
        item['horse_name'] = ['ミヤビホウリキ\xa0']
        item['horse_url'] = ['https://www.oddspark.com/keiba/HorseDetail.do?lineageNb=2280190375']
        item['owner'] = ['中島雅也']
        item['parent_horse_name_1'] = ['アサノカイリキ\u200b']
        item['parent_horse_name_2'] = ['千\u3000花\u200b']
        item['trainer_url'] = ['/keiba/TrainerDetail.do?trainerNb=018052']

        # Before check
        self.pipeline.db_cursor.execute("select * from horse")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from horse")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['birthday'], '2016年3月30日')
        eq_(record['breeder'], '橋\u3000本\u3000岩\u3000雄')
        eq_(record['breeding_farm'], '北海道日高郡新ひだか町')
        eq_(record['coat_color'], '栗毛')
        eq_(record['gender_age'], '牡｜4 歳')
        eq_(record['grand_parent_horse_name_1'], 'ハイパワード\u200b')
        eq_(record['grand_parent_horse_name_2'], 'スーパーマコト\u200b')
        eq_(record['grand_parent_horse_name_3'], '肖\u3000命\u200b')
        eq_(record['grand_parent_horse_name_4'], '宝\u3000秀\u200b')
        eq_(record['horse_name'], 'ミヤビホウリキ\xa0')
        eq_(record['horse_url'], 'https://www.oddspark.com/keiba/HorseDetail.do?lineageNb=2280190375')
        eq_(record['owner'], '中島雅也')
        eq_(record['parent_horse_name_1'], 'アサノカイリキ\u200b')
        eq_(record['parent_horse_name_2'], '千\u3000花\u200b')
        eq_(record['trainer_url'], '/keiba/TrainerDetail.do?trainerNb=018052')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from horse")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_jockey_item_1(self):
        # Setup
        item = JockeyItem()
        item['belong_to'] = ['ばんえい']
        item['birthday'] = ['1983年9月23日']
        item['first_licensing_year'] = ['2007年']
        item['gender'] = ['男']
        item['jockey_name'] = ['船\u3000山\u3000\u3000蔵\u3000人\xa0']
        item['jockey_url'] = ['https://www.oddspark.com/keiba/JockeyDetail.do?jkyNb=038071']
        item['trainer_url'] = ['/keiba/TrainerDetail.do?trainerNb=018017']

        # Before check
        self.pipeline.db_cursor.execute("select * from jockey")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from jockey")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['belong_to'], 'ばんえい')
        eq_(record['birthday'], '1983年9月23日')
        eq_(record['first_licensing_year'], '2007年')
        eq_(record['gender'], '男')
        eq_(record['jockey_name'], '船\u3000山\u3000\u3000蔵\u3000人\xa0')
        eq_(record['jockey_url'], 'https://www.oddspark.com/keiba/JockeyDetail.do?jkyNb=038071')
        eq_(record['trainer_url'], '/keiba/TrainerDetail.do?trainerNb=018017')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from jockey")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_trainer_item_1(self):
        # Setup
        item = TrainerItem()
        item['belong_to'] = ['ばんえい']
        item['birthday'] = ['1959年1月2日']
        item['gender'] = ['男']
        item['trainer_name'] = ['小\u3000林\u3000\u3000勝\u3000二\xa0']
        item['trainer_url'] = ['https://www.oddspark.com/keiba/TrainerDetail.do?trainerNb=018052']

        # Before check
        self.pipeline.db_cursor.execute("select * from trainer")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from trainer")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['belong_to'], 'ばんえい')
        eq_(record['birthday'], '1959年1月2日')
        eq_(record['gender'], '男')
        eq_(record['trainer_name'], '小\u3000林\u3000\u3000勝\u3000二\xa0')
        eq_(record['trainer_url'], 'https://www.oddspark.com/keiba/TrainerDetail.do?trainerNb=018052')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from trainer")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_win_place_item_1(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_number'] = ['1']
        item['horse_url'] = ['/keiba/HorseDetail.do?lineageNb=2280190375']
        item['odds_place'] = ['1.0 - 1.2']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1']
        item['odds_win'] = ['5.5']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_win_place")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_win_place")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number'], '1')
        eq_(record['horse_url'], '/keiba/HorseDetail.do?lineageNb=2280190375')
        eq_(record['odds_place'], '1.0 - 1.2')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1')
        eq_(record['odds_win'], '5.5')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_win_place")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_quinella_item_1(self):
        # Setup
        item = OddsQuinellaItem()
        item['horse_number_1'] = ['1']
        item['horse_number_2'] = ['2']
        item['odds'] = ['20.0']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1&betType=6']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_quinella")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_quinella")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number_1'], '1')
        eq_(record['horse_number_2'], '2')
        eq_(record['odds'], '20.0')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1&betType=6')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_quinella")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_exacta_item_1(self):
        # Setup
        item = OddsExactaItem()
        item['horse_number_1'] = ['2']
        item['horse_number_2'] = ['1']
        item['odds'] = ['26.0']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=8&betType=5']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_exacta")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_exacta")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number_1'], '2')
        eq_(record['horse_number_2'], '1')
        eq_(record['odds'], '26.0')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=8&betType=5')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_exacta")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_quinella_place_item_1(self):
        # Setup
        item = OddsQuinellaPlaceItem()
        item['horse_number_1'] = ['1']
        item['horse_number_2'] = ['2']
        item['odds_lower'] = ['3.8']
        item['odds_upper'] = ['4.1']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=8&betType=7']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_quinella_place")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_quinella_place")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number_1'], '1')
        eq_(record['horse_number_2'], '2')
        eq_(record['odds_lower'], '3.8')
        eq_(record['odds_upper'], '4.1')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=8&betType=7')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_quinella_place")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_trio_item_1(self):
        # Setup
        item = OddsTrioItem()
        item['horse_number_1_2'] = ['1-2']
        item['horse_number_3'] = ['3']
        item['odds'] = ['197.7']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=06&raceDy=20201018&opTrackCd=11&raceNb=7&betType=9']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_trio")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_trio")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number_1_2'], '1-2')
        eq_(record['horse_number_3'], '3')
        eq_(record['odds'], '197.7')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=06&raceDy=20201018&opTrackCd=11&raceNb=7&betType=9')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_trio")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

    def test_process_odds_trifecta_item_1(self):
        # Setup
        item = OddsTrifectaItem()
        item['horse_number'] = ['1 → 2 → 3']
        item['odds'] = ['1275.9']
        item['odds_url'] = ['https://www.oddspark.com/keiba/Odds.do?sponsorCd=06&raceDy=20201018&opTrackCd=11&raceNb=7&betType=8&horseNb=1']

        # Before check
        self.pipeline.db_cursor.execute("select * from odds_trifecta")
        eq_(len(self.pipeline.db_cursor.fetchall()), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        self.pipeline.db_cursor.execute("select * from odds_trifecta")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record['id']), 64)
        eq_(record['horse_number'], '1 → 2 → 3')
        eq_(record['odds'], '1275.9')
        eq_(record['odds_url'], 'https://www.oddspark.com/keiba/Odds.do?sponsorCd=06&raceDy=20201018&opTrackCd=11&raceNb=7&betType=8&horseNb=1')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        self.pipeline.db_cursor.execute("select * from odds_trifecta")

        records = self.pipeline.db_cursor.fetchall()
        eq_(len(records), 1)
