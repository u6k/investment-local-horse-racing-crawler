import scrapy


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    start_urls = [
        "https://www.oddspark.com/keiba/KaisaiCalendar.do",
    ]

    def parse(self, response):
        """ Parse calendar page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do
        @returns items 0 0
        @returns requests 1
        @schedule_list
        """

        self.logger.info(f"#parse: start: url={response.url}")

        for a in response.xpath("//ul[@id='date_pr']/li/a"):
            self.logger.info("#parse: found previous calendar page: href=%s" % a.xpath("@href").get())
            yield response.follow(a, callback=self.parse)

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href.startswith("/keiba/RaceRefund.do?"):
                self.logger.info(f"#parse: found race refund list page: href={href}")
                yield response.follow(a, callback=self.parse_race_refund_list)

    def parse_race_refund_list(self, response):
        """ Parse race refund list page.

        @url https://www.oddspark.com/keiba/RaceRefund.do?opTrackCd=03&raceDy=20200301&sponsorCd=04
        @returns items 0 0
        @returns requests 1
        @race_refund_list
        """

        self.logger.info(f"#parse_race_refund_list: start: url={response.url}")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is not None and href.startswith("/keiba/RaceList.do?"):
                self.logger.info(f"#parse_race_refund_list: found race denma page: href={href}")
                yield response.follow(a, callback=self.parse_race_denma)

    def parse_race_denma(self, response):
        """ Parse race denma page.

        @url https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 0 0
        @returns requests 1
        @race_denma
        """

        self.logger.info(f"#parse_race_denma: start: url={response.url}")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is None:
                continue

            if href.startswith("/keiba/Odds.do?"):
                self.logger.info(f"#parse_race_denma: found odds page: href={href}")
                yield response.follow(a, callback=self.parse_odds_win)

            if href.startswith("/keiba/RaceResult.do?"):
                self.logger.info(f"#parse_race_denma: found race result page: href={href}")
                yield response.follow(a, callback=self.parse_race_result)

            if href.startswith("/keiba/HorseDetail.do?"):
                self.logger.info(f"#parse_race_denma: found horse page: href={href}")
                yield response.follow(a, callback=self.parse_horse)

            if href.startswith("/keiba/JockeyDetail.do?"):
                self.logger.info(f"#parse_race_denma: found jockey page: href={href}")
                yield response.follow(a, callback=self.parse_jockey)

            if href.startswith("/keiba/TrainerDetail.do?"):
                self.logger.info(f"#parse_race_denma: found trainer page: href={href}")
                yield response.follow(a, callback=self.parse_trainer)

    def parse_odds_win(self, response):
        """ Parse odds(win) page.

        @url https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 0 0
        @returns requests 0
        @odds_win
        """

        self.logger.info(f"#parse_odds_win: start: url={response.url}")

    def parse_race_result(self, response):
        """ Parse race result page.

        @url https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 0 0
        @returns requests 0
        @race_result
        """

        self.logger.info(f"#parse_race_result: start: url={response.url}")

    def parse_horse(self, response):
        """ Parse horse page.

        @url https://www.oddspark.com/keiba/HorseDetail.do?lineageNb=2280190375
        @returns items 0 0
        @returns requests 0 0
        @horse
        """

        self.logger.info(f"#parse_horse: start: url={response.url}")

    def parse_jockey(self, response):
        """ Parse jockey page.

        @url https://www.oddspark.com/keiba/JockeyDetail.do?jkyNb=038071
        @returns items 0 0
        @returns requests 0 0
        @jockey
        """

        self.logger.info(f"#parse_jockey: start: url={response.url}")

    def parse_trainer(self, response):
        """ Parse trainer page.
        """

        self.logger.info(f"#parse_trainer: start: url={response.url}")
