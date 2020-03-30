import scrapy
from scrapy.loader import ItemLoader

from investment_local_horse_racing_crawler.items import RaceInfoItem, RaceDenmaItem


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
        @returns items 1
        @returns requests 1
        @race_denma
        """

        self.logger.info(f"#parse_race_denma: start: url={response.url}")

        # Parse race info
        self.logger.debug("#parse_race_denma: parse race info")

        loader = ItemLoader(item=RaceInfoItem(), response=response)
        race_id = response.url.split("?")[-1]
        loader.add_value("race_id", race_id)
        loader.add_xpath("race_round", "//div[@id='RCdata1']/span/text()")
        loader.add_xpath("race_name", "//div[@id='RCdata2']/h3/text()")
        loader.add_xpath("start_date", "//div[@id='RCdata2']/ul/li[@class='RCdate']/text()")
        loader.add_xpath("place_name", "//div[@id='RCdata2']/ul/li[@class='RCnum']/text()")
        loader.add_xpath("course_type_length", "//div[@id='RCdata2']/ul/li[@class='RCdst']/text()")
        loader.add_xpath("start_time", "//div[@id='RCdata2']/ul/li[@class='RCstm']/text()")
        loader.add_xpath("weather", "//div[@id='RCdata2']/ul/li[@class='RCwthr']/img/@src")
        loader.add_xpath("moisture", "//div[@id='RCdata2']/ul/li[@class='RCwatr']/span[@class='baba']/text()")
        loader.add_xpath("added_money", "//div[@id='RCdata2']/p/text()")
        i = loader.load_item()

        self.logger.info(f"#parse_race_denma: race info={i}")
        yield i

        # Parse race denma
        self.logger.debug("#parse_race_denma: parse race denma")

        for tr in response.xpath("//table[contains(@class,'ent1')]/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            if len(tr.xpath("td")) == 15:
                bracket_number = tr.xpath("td[1]/text()").get()

                loader = ItemLoader(item=RaceDenmaItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("bracket_number", bracket_number)
                loader.add_xpath("horse_number", "td[3]/text()")
                loader.add_xpath("horse_id", "td[5]/a/@href")
                loader.add_xpath("jockey_id", "td[6]/a[1]/@href")
                loader.add_xpath("jockey_weight", "td[6]/strong/text()")
                loader.add_xpath("trainer_id", "td[6]/a[2]/@href")
                loader.add_xpath("odds_win", "td[7]/span/text()")
                loader.add_xpath("favorite", "td[7]/text()")
                loader.add_xpath("horse_weight", "td[8]/text()[1]")
                loader.add_xpath("horse_weight_diff", "td[8]/text()[2]")
                i = loader.load_item()

                self.logger.info(f"#parse_race_denma: race denma={i}")
                yield i
            elif len(tr.xpath("td")) == 13:
                loader = ItemLoader(item=RaceDenmaItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("bracket_number", bracket_number)
                loader.add_xpath("horse_number", "td[1]/text()")
                loader.add_xpath("horse_id", "td[3]/a/@href")
                loader.add_xpath("jockey_id", "td[4]/a[1]/@href")
                loader.add_xpath("jockey_weight", "td[4]/strong/text()")
                loader.add_xpath("trainer_id", "td[4]/a[2]/@href")
                loader.add_xpath("odds_win", "td[5]/span/text()")
                loader.add_xpath("favorite", "td[5]/text()")
                loader.add_xpath("horse_weight", "td[6]/text()[1]")
                loader.add_xpath("horse_weight_diff", "td[6]/text()[2]")
                i = loader.load_item()

                self.logger.info(f"#parse_race_denma: race denma={i}")
                yield i
            else:
                self.logger.warn("#parse_race_denma: unknown record")

        # Parse link
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

        @url https://www.oddspark.com/keiba/TrainerDetail.do?trainerNb=018052
        @returns items 0 0
        @returns requests 0 0
        @trainer
        """

        self.logger.info(f"#parse_trainer: start: url={response.url}")
