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
            "start_date": "2018-01-01",
            "end_date": "2018-01-02",
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

        assert len(race_infos) == 35
        assert race_infos[0]["race_id"] == "raceDy=20180101&raceNb=1&opTrackCd=43&sponsorCd=33"
        assert race_infos[1]["race_id"] == "raceDy=20180101&raceNb=2&opTrackCd=43&sponsorCd=33"
        assert race_infos[2]["race_id"] == "raceDy=20180101&raceNb=1&opTrackCd=03&sponsorCd=04"
        assert race_infos[3]["race_id"] == "raceDy=20180101&raceNb=3&opTrackCd=43&sponsorCd=33"
        assert race_infos[4]["race_id"] == "raceDy=20180101&raceNb=2&opTrackCd=03&sponsorCd=04"
        assert race_infos[5]["race_id"] == "raceDy=20180101&raceNb=4&opTrackCd=43&sponsorCd=33"
        assert race_infos[6]["race_id"] == "raceDy=20180101&raceNb=3&opTrackCd=03&sponsorCd=04"
        assert race_infos[7]["race_id"] == "raceDy=20180101&raceNb=5&opTrackCd=43&sponsorCd=33"
        assert race_infos[8]["race_id"] == "raceDy=20180101&raceNb=1&opTrackCd=55&sponsorCd=29"
        assert race_infos[9]["race_id"] == "raceDy=20180101&raceNb=6&opTrackCd=43&sponsorCd=33"
        assert race_infos[10]["race_id"] == "raceDy=20180101&raceNb=4&opTrackCd=03&sponsorCd=04"
        assert race_infos[11]["race_id"] == "raceDy=20180101&raceNb=2&opTrackCd=55&sponsorCd=29"
        assert race_infos[12]["race_id"] == "raceDy=20180101&raceNb=7&opTrackCd=43&sponsorCd=33"
        assert race_infos[13]["race_id"] == "raceDy=20180101&raceNb=5&opTrackCd=03&sponsorCd=04"
        assert race_infos[14]["race_id"] == "raceDy=20180101&raceNb=3&opTrackCd=55&sponsorCd=29"
        assert race_infos[15]["race_id"] == "raceDy=20180101&raceNb=8&opTrackCd=43&sponsorCd=33"
        assert race_infos[16]["race_id"] == "raceDy=20180101&raceNb=6&opTrackCd=03&sponsorCd=04"
        assert race_infos[17]["race_id"] == "raceDy=20180101&raceNb=4&opTrackCd=55&sponsorCd=29"
        assert race_infos[18]["race_id"] == "raceDy=20180101&raceNb=9&opTrackCd=43&sponsorCd=33"
        assert race_infos[19]["race_id"] == "raceDy=20180101&raceNb=7&opTrackCd=03&sponsorCd=04"
        assert race_infos[20]["race_id"] == "raceDy=20180101&raceNb=5&opTrackCd=55&sponsorCd=29"
        assert race_infos[21]["race_id"] == "raceDy=20180101&raceNb=10&opTrackCd=43&sponsorCd=33"
        assert race_infos[22]["race_id"] == "raceDy=20180101&raceNb=8&opTrackCd=03&sponsorCd=04"
        assert race_infos[23]["race_id"] == "raceDy=20180101&raceNb=6&opTrackCd=55&sponsorCd=29"
        assert race_infos[24]["race_id"] == "raceDy=20180101&raceNb=11&opTrackCd=43&sponsorCd=33"
        assert race_infos[25]["race_id"] == "raceDy=20180101&raceNb=9&opTrackCd=03&sponsorCd=04"
        assert race_infos[26]["race_id"] == "raceDy=20180101&raceNb=7&opTrackCd=55&sponsorCd=29"
        assert race_infos[27]["race_id"] == "raceDy=20180101&raceNb=12&opTrackCd=43&sponsorCd=33"
        assert race_infos[28]["race_id"] == "raceDy=20180101&raceNb=10&opTrackCd=03&sponsorCd=04"
        assert race_infos[29]["race_id"] == "raceDy=20180101&raceNb=8&opTrackCd=55&sponsorCd=29"
        assert race_infos[30]["race_id"] == "raceDy=20180101&raceNb=11&opTrackCd=03&sponsorCd=04"
        assert race_infos[31]["race_id"] == "raceDy=20180101&raceNb=9&opTrackCd=55&sponsorCd=29"
        assert race_infos[32]["race_id"] == "raceDy=20180101&raceNb=10&opTrackCd=55&sponsorCd=29"
        assert race_infos[33]["race_id"] == "raceDy=20180101&raceNb=11&opTrackCd=55&sponsorCd=29"
        assert race_infos[34]["race_id"] == "raceDy=20180101&raceNb=12&opTrackCd=55&sponsorCd=29"

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
