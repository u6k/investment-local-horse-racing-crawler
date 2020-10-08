# TODO: Scrapyコマンドのテストに変更する

import logging

from investment_local_horse_racing_crawler import flask, VERSION


class TestFlask:
    def setUp(self):
        logging.disable(logging.DEBUG)

        self.app = flask.app.test_client()

        with flask.get_db() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("delete from race_info")
                db_cursor.execute("delete from race_denma")
                db_cursor.execute("delete from race_payoff")
                db_cursor.execute("delete from race_result")
                db_cursor.execute("delete from odds_win")
                db_cursor.execute("delete from odds_place")
                db_cursor.execute("delete from horse")
                db_cursor.execute("delete from jockey")
                db_cursor.execute("delete from trainer")

                db_conn.commit()

    def test_health(self):
        # Execute
        result = self.app.get("/api/health")

        # Check
        assert result.status_code == 200

        result_data = result.get_json()
        assert result_data["version"] == VERSION

    def test_crawl_1(self):
        # Setup
        req_data = {
            "start_url": "https://www.oddspark.com/keiba/KaisaiCalendar.do?target=201801",
            "start_date": "2018-01-06",
            "end_date": "2018-01-07",
            "recache_race": False,
            "recache_horse": False,
        }

        # Execute
        result = self.app.post("/api/crawl", json=req_data)

        # Check
        assert result.status_code == 200

        result_data = result.get_json()
        assert result_data["result"]

        with flask.get_db().cursor() as db_cursor:
            db_cursor.execute("select race_id from race_info order by start_datetime, race_id")
            race_infos = db_cursor.fetchall()

        assert len(race_infos) == 10
        assert race_infos[0]["race_id"] == "raceDy=20180106&raceNb=1&opTrackCd=12&sponsorCd=06"
        assert race_infos[1]["race_id"] == "raceDy=20180106&raceNb=2&opTrackCd=12&sponsorCd=06"
        assert race_infos[2]["race_id"] == "raceDy=20180106&raceNb=3&opTrackCd=12&sponsorCd=06"
        assert race_infos[3]["race_id"] == "raceDy=20180106&raceNb=4&opTrackCd=12&sponsorCd=06"
        assert race_infos[4]["race_id"] == "raceDy=20180106&raceNb=5&opTrackCd=12&sponsorCd=06"
        assert race_infos[5]["race_id"] == "raceDy=20180106&raceNb=6&opTrackCd=12&sponsorCd=06"
        assert race_infos[6]["race_id"] == "raceDy=20180106&raceNb=7&opTrackCd=12&sponsorCd=06"
        assert race_infos[7]["race_id"] == "raceDy=20180106&raceNb=8&opTrackCd=12&sponsorCd=06"
        assert race_infos[8]["race_id"] == "raceDy=20180106&raceNb=9&opTrackCd=12&sponsorCd=06"
        assert race_infos[9]["race_id"] == "raceDy=20180106&raceNb=10&opTrackCd=12&sponsorCd=06"

        # Setup (2)
        req_data = {
            "target_date": "2018-01-06",
        }

        # Execute (2)
        result = self.app.post("/api/schedule_vote_close", json=req_data)

        # Check (2)
        assert result.status_code == 200

        result_data = result.get_json()
        races = result_data["races"]
        assert len(races) == 10

        assert races[0]["race_id"] == "raceDy=20180106&raceNb=1&opTrackCd=12&sponsorCd=06"
        assert races[0]["start_datetime"] == "2018-01-06 10:30:00"

        assert races[1]["race_id"] == "raceDy=20180106&raceNb=2&opTrackCd=12&sponsorCd=06"
        assert races[1]["start_datetime"] == "2018-01-06 11:05:00"

        assert races[2]["race_id"] == "raceDy=20180106&raceNb=3&opTrackCd=12&sponsorCd=06"
        assert races[2]["start_datetime"] == "2018-01-06 11:40:00"

        assert races[3]["race_id"] == "raceDy=20180106&raceNb=4&opTrackCd=12&sponsorCd=06"
        assert races[3]["start_datetime"] == "2018-01-06 12:15:00"

        assert races[4]["race_id"] == "raceDy=20180106&raceNb=5&opTrackCd=12&sponsorCd=06"
        assert races[4]["start_datetime"] == "2018-01-06 12:50:00"

        assert races[5]["race_id"] == "raceDy=20180106&raceNb=6&opTrackCd=12&sponsorCd=06"
        assert races[5]["start_datetime"] == "2018-01-06 13:25:00"

        assert races[6]["race_id"] == "raceDy=20180106&raceNb=7&opTrackCd=12&sponsorCd=06"
        assert races[6]["start_datetime"] == "2018-01-06 14:00:00"

        assert races[7]["race_id"] == "raceDy=20180106&raceNb=8&opTrackCd=12&sponsorCd=06"
        assert races[7]["start_datetime"] == "2018-01-06 14:35:00"

        assert races[8]["race_id"] == "raceDy=20180106&raceNb=9&opTrackCd=12&sponsorCd=06"
        assert races[8]["start_datetime"] == "2018-01-06 15:15:00"

        assert races[9]["race_id"] == "raceDy=20180106&raceNb=10&opTrackCd=12&sponsorCd=06"
        assert races[9]["start_datetime"] == "2018-01-06 15:50:00"

    def test_crawl_2(self):
        # Setup
        req_data = {
            "start_url": "https://www.oddspark.com/keiba/RaceList.do?sponsorCd=33&raceDy=20180101&opTrackCd=43&raceNb=2",
            "recache_race": True,
            "recache_horse": False,
        }

        # Execute
        result = self.app.post("/api/crawl", json=req_data)

        # Check
        assert result.status_code == 200

        result_data = result.get_json()
        assert result_data["result"]

        with flask.get_db().cursor() as db_cursor:
            db_cursor.execute("select race_id from race_info order by start_datetime")
            race_infos = db_cursor.fetchall()

        assert len(race_infos) == 1
        assert race_infos[0]["race_id"] == "raceDy=20180101&raceNb=2&opTrackCd=43&sponsorCd=33"
