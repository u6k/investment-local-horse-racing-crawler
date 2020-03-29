import scrapy


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    start_urls = [
        "https://www.oddspark.com/keiba/KaisaiCalendar.do",
    ]

    def parse(self, response):
        """ Parse calendar page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do
        @returns items 0
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
        @returns items 0
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
        """

        self.logger.info(f"#parse_race_denma: start: url={response.url}")
