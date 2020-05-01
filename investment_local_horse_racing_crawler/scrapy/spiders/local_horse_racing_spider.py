import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import scrapy
from scrapy.loader import ItemLoader

from investment_local_horse_racing_crawler.scrapy.items import RaceInfoItem, RaceDenmaItem, OddsWinPlaceItem, RaceResultItem, RacePayoffItem, HorseItem, JockeyItem, TrainerItem
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    def __init__(self, start_url="https://www.oddspark.com/keiba/KaisaiCalendar.do", recrawl_period="all", recrawl_race_id=None, recache_race=False, recache_horse=False, *args, **kwargs):
        super(LocalHorseRacingSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_url]

        if recrawl_period == "all":
            recrawl_period = 100000
        recrawl_period = int(recrawl_period)
        self.recrawl_end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0, 0) + timedelta(days=1)
        self.recrawl_start_date = self.recrawl_end_date - timedelta(days=recrawl_period)

        self.recrawl_race_id = recrawl_race_id
        self.recache_race = recache_race
        self.recache_horse = recache_horse

    def parse(self, response):
        """ Parse calendar page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do?target=202004
        @returns items 0 0
        @returns requests 1
        @schedule_list
        """

        logger.info(f"#parse: start: url={response.url}")

        logger.info(f"#parse: recrawl_start_date={self.recrawl_start_date}")
        logger.info(f"#parse: recrawl_end_date={self.recrawl_end_date}")
        logger.info(f"#parse: recrawl_race_id={self.recrawl_race_id}")
        logger.info(f"#parse: recache_race={self.recache_race}")
        logger.info(f"#parse: recache_horse={self.recache_horse}")

        if self.recrawl_race_id:
            logger.info(f"#parse: re-crawl race: {self.recrawl_race_id}")

            url = f"https://www.oddspark.com/keiba/RaceList.do?{self.recrawl_race_id}"
            yield response.follow(url, callback=self.parse_race_denma)

            return

        for a in response.xpath("//ul[@id='date_pr']/li/a"):
            logger.info("#parse: found previous calendar page: href=%s" % a.xpath("@href").get())

            # Check re-crawl
            target_re = re.match("^.*target=([0-9]{6})$", a.xpath("@href").get())
            if target_re:
                target_start = datetime(int(target_re.group(1)[0:4]), int(target_re.group(1)[4:6]), 1, 0, 0, 0)
                target_end = target_start + relativedelta(months=1)

                if not (self.recrawl_start_date <= target_end and self.recrawl_end_date >= target_start):
                    logger.info(f"#parse: cancel previous calendar page: target={target_start} to {target_end}, settings={self.recrawl_start_date} to {self.recrawl_end_date}")
                    continue

            yield response.follow(a, callback=self.parse)

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href.startswith("/keiba/RaceRefund.do?"):
                logger.info(f"#parse: found race refund list page: href={href}")

                # Check re-crawl
                target_re = re.match("^.*raceDy=([0-9]{8}).*$", href)
                if target_re:
                    target_date = datetime(int(target_re.group(1)[0:4]), int(target_re.group(1)[4:6]), int(target_re.group(1)[6:8]), 0, 0, 0)

                    if not (self.recrawl_start_date <= target_date < self.recrawl_end_date):
                        logger.info(f"#parse: cancel race refund list: target={target_date}, settings={self.recrawl_start_date} to {self.recrawl_end_date}")
                        continue

                yield response.follow(a, callback=self.parse_race_refund_list)

            if href.startswith("/keiba/OneDayRaceList.do?"):
                logger.info(f"#parse: found one day race list page: href={href}")

                # Check re-crawl
                target_re = re.match("^.*raceDy=([0-9]{8}).*$", href)
                if target_re:
                    target_date = datetime(int(target_re.group(1)[0:4]), int(target_re.group(1)[4:6]), int(target_re.group(1)[6:8]), 0, 0, 0)

                    if not (self.recrawl_start_date <= target_date < self.recrawl_end_date):
                        logger.info(f"#parse: cancel one day race list: target={target_date}, settings={self.recrawl_start_date} to {self.recrawl_end_date}")
                        continue

                yield response.follow(a, callback=self.parse_one_day_race_list)

    def parse_race_refund_list(self, response):
        """ Parse race refund list page.

        @url https://www.oddspark.com/keiba/RaceRefund.do?opTrackCd=03&raceDy=20200301&sponsorCd=04
        @returns items 0 0
        @returns requests 1
        @race_refund_list
        """

        logger.info(f"#parse_race_refund_list: start: url={response.url}")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is not None and href.startswith("/keiba/RaceList.do?"):
                logger.info(f"#parse_race_refund_list: found race denma page: href={href}")
                yield response.follow(a, callback=self.parse_race_denma)

    def parse_one_day_race_list(self, response):
        """ Parse one day race list page.

        @url https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200417&sponsorCd=20
        @returns items 0 0
        @returns requests 1
        @one_day_race_list
        """

        logger.info(f"#parse_one_day_race_list: start: url={response.url}")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is not None and href.startswith("/keiba/RaceList.do?raceDy="):
                logger.info(f"#parse_one_day_race_list: found race denma page: href={href}")
                yield response.follow(a, callback=self.parse_race_denma)

    def parse_race_denma(self, response):
        """ Parse race denma page.

        @url https://www.oddspark.com/keiba/RaceList.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 1
        @returns requests 1
        @race_denma
        """

        logger.info(f"#parse_race_denma: start: url={response.url}")

        # Parse race info
        logger.debug("#parse_race_denma: parse race info")

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

        logger.info(f"#parse_race_denma: race info={i}")
        yield i

        # Parse race denma
        logger.debug("#parse_race_denma: parse race denma")

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

                logger.info(f"#parse_race_denma: race denma={i}")
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

                logger.info(f"#parse_race_denma: race denma={i}")
                yield i
            else:
                logger.warn("#parse_race_denma: unknown record")

        # Parse link
        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is None:
                continue

            if href.startswith("/keiba/Odds.do?"):
                logger.info(f"#parse_race_denma: found odds page: href={href}")
                yield response.follow(a, callback=self.parse_odds_win)

            if href.startswith("/keiba/RaceResult.do?"):
                logger.info(f"#parse_race_denma: found race result page: href={href}")
                yield response.follow(a, callback=self.parse_race_result)

            if href.startswith("/keiba/HorseDetail.do?"):
                logger.info(f"#parse_race_denma: found horse page: href={href}")
                yield response.follow(a, callback=self.parse_horse)

            if href.startswith("/keiba/JockeyDetail.do?"):
                logger.info(f"#parse_race_denma: found jockey page: href={href}")
                yield response.follow(a, callback=self.parse_jockey)

            if href.startswith("/keiba/TrainerDetail.do?"):
                logger.info(f"#parse_race_denma: found trainer page: href={href}")
                yield response.follow(a, callback=self.parse_trainer)

    def parse_odds_win(self, response):
        """ Parse odds(win) page.

        @url https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 1
        @returns requests 0 0
        @odds_win
        """

        logger.info(f"#parse_odds_win: start: url={response.url}")

        # Parse odds win/place
        logger.debug("#parse_odds_win: parse odds win/place")

        race_id = response.url.split("?")[-1]

        for tr in response.xpath("//table[contains(@class,'tb71')]/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            loader = ItemLoader(item=OddsWinPlaceItem(), selector=tr)

            if len(tr.xpath("td")) == 5:
                loader.add_value("race_id", race_id)
                loader.add_xpath("horse_number", "td[2]/text()")
                loader.add_xpath("horse_id", "td[3]/a/@href")
                loader.add_xpath("odds_win", "td[4]/span/text()")
                loader.add_xpath("odds_place_min", "td[5]/span[1]/text()")
                loader.add_xpath("odds_place_max", "td[5]/span[2]/text()")
            elif len(tr.xpath("td")) == 4:
                loader.add_value("race_id", race_id)
                loader.add_xpath("horse_number", "td[1]/text()")
                loader.add_xpath("horse_id", "td[2]/a/@href")
                loader.add_xpath("odds_win", "td[3]/span/text()")
                loader.add_xpath("odds_place_min", "td[4]/span[1]/text()")
                loader.add_xpath("odds_place_max", "td[4]/span[2]/text()")
            else:
                logger.warn("Unknown record")
                continue

            i = loader.load_item()

            logger.info(f"#parse_odds_win: odds win/place={i}")
            yield i

    def parse_race_result(self, response):
        """ Parse race result page.

        @url https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 1
        @returns requests 0 0
        @race_result
        """

        logger.info(f"#parse_race_result: start: url={response.url}")

        # Parse race result
        logger.debug("#parse_race_result: parse race result")

        race_id = response.url.split("?")[-1]

        for tr in response.xpath("//table[@summary='レース結果']/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            loader = ItemLoader(item=RaceResultItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_xpath("result", "td[1]/text()")
            loader.add_xpath("bracket_number", "td[2]/text()")
            loader.add_xpath("horse_number", "td[3]/text()")
            loader.add_xpath("horse_id", "td[4]/a/@href")
            loader.add_xpath("arrival_time", "td[11]/text()")
            i = loader.load_item()

            logger.info(f"#parse_race_result: race result={i}")
            yield i

        # Parse race result
        logger.debug("#parse_race_result: parse race payoff")

        for tr in response.xpath("//table[@summary='払戻金情報']/tr"):
            if len(tr.xpath("th")) > 0:
                payoff_type = tr.xpath("th/text()").get()

            loader = ItemLoader(item=RacePayoffItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_value("payoff_type", payoff_type)
            loader.add_xpath("horse_number", "td[1]/text()")
            loader.add_xpath("odds", "td[2]/text()")
            loader.add_xpath("favorite", "td[3]/text()")
            i = loader.load_item()

            logger.info(f"#parse_race_result: race payoff={i}")
            yield i

    def parse_horse(self, response):
        """ Parse horse page.

        @url https://www.oddspark.com/keiba/HorseDetail.do?lineageNb=2280190375
        @returns items 1 1
        @returns requests 0 0
        @horse
        """

        logger.info(f"#parse_horse: start: url={response.url}")

        # Parse horse
        logger.debug("#parse_horse: parse horse")

        loader = ItemLoader(item=HorseItem(), response=response)
        loader.add_value("horse_id", response.url.split("?")[-1])
        loader.add_xpath("horse_name", "//div[@id='content']/div[2]/span[1]/text()")
        loader.add_xpath("gender_age", "//div[@id='content']/div[2]/span[2]/text()")

        if response.xpath("//table[contains(@class,'tb72')]/tr[1]/th/text()").get() != "生年月日":
            raise RuntimeError("Unknown header birthday")
        else:
            loader.add_xpath("birthday", "//table[contains(@class,'tb72')]/tr[1]/td/text()")

        if response.xpath("//table[contains(@class,'tb72')]/tr[2]/th/text()").get() != "毛色":
            raise RuntimeError("Unknown header coat_color")
        else:
            loader.add_xpath("coat_color", "//table[contains(@class,'tb72')]/tr[2]/td/text()")

        if response.xpath("//table[contains(@class,'tb72')]/tr[4]/th/text()").get() != "馬主":
            raise RuntimeError("Unknown header owner")
        else:
            loader.add_xpath("owner", "//table[contains(@class,'tb72')]/tr[4]/td/text()")

        if response.xpath("//table[contains(@class,'tb72')]/tr[5]/th/text()").get() != "生産者":
            raise RuntimeError("Unknown header breeder")
        else:
            loader.add_xpath("breeder", "//table[contains(@class,'tb72')]/tr[5]/td/text()")

        if response.xpath("//table[contains(@class,'tb72')]/tr[6]/th/text()").get() != "産地":
            raise RuntimeError("Unknown header breeding_farm")
        else:
            loader.add_xpath("breeding_farm", "//table[contains(@class,'tb72')]/tr[6]/td/text()")

        if response.xpath("//table[contains(@class,'tb71')]/tr[1]/td/text()").get() != "血統":
            raise RuntimeError("Unknown table parents")

        loader.add_xpath("parent_horse_name_1", "//table[contains(@class,'tb71')]/tr[2]/td[1]/text()")
        loader.add_xpath("parent_horse_name_2", "//table[contains(@class,'tb71')]/tr[4]/td[1]/text()")
        loader.add_xpath("grand_parent_horse_name_1", "//table[contains(@class,'tb71')]/tr[2]/td[2]/text()")
        loader.add_xpath("grand_parent_horse_name_2", "//table[contains(@class,'tb71')]/tr[3]/td[1]/text()")
        loader.add_xpath("grand_parent_horse_name_3", "//table[contains(@class,'tb71')]/tr[4]/td[2]/text()")
        loader.add_xpath("grand_parent_horse_name_4", "//table[contains(@class,'tb71')]/tr[5]/td[1]/text()")
        i = loader.load_item()

        logger.info(f"#parse_horse: horse={i}")
        yield i

    def parse_jockey(self, response):
        """ Parse jockey page.

        @url https://www.oddspark.com/keiba/JockeyDetail.do?jkyNb=038071
        @returns items 1 1
        @returns requests 0 0
        @jockey
        """

        logger.info(f"#parse_jockey: start: url={response.url}")

        # Parse jockey
        logger.debug("#parse_jockey: parse jockey")

        loader = ItemLoader(item=JockeyItem(), response=response)
        loader.add_value("jockey_id", response.url.split("?")[-1])
        loader.add_xpath("jockey_name", "//div[@id='content']/div[2]/span[1]/text()")

        table = response.xpath("//table[contains(@class,'tb72')]")[0]

        if table.xpath("tr[1]/th/text()").get() != "生年月日":
            raise RuntimeError("Unknown header birthday")
        else:
            loader.add_value("birthday", table.xpath("tr[1]/td/text()").get())

        if table.xpath("tr[2]/th/text()").get() != "性別":
            raise RuntimeError("Unknown header gender")
        else:
            loader.add_value("gender", table.xpath("tr[2]/td/text()").get())

        if table.xpath("tr[3]/th/text()").get() != "所属":
            raise RuntimeError("Unknown header belong_to")
        else:
            loader.add_value("belong_to", table.xpath("tr[3]/td/text()").get())

        if table.xpath("tr[5]/th/text()").get() != "初免許年":
            raise RuntimeError("Unknown header first_licensing_year")
        else:
            loader.add_value("first_licensing_year", table.xpath("tr[5]/td/text()").get())

        i = loader.load_item()

        logger.info(f"#parse_jockey: jockey={i}")
        yield i

    def parse_trainer(self, response):
        """ Parse trainer page.

        @url https://www.oddspark.com/keiba/TrainerDetail.do?trainerNb=018052
        @returns items 1 1
        @returns requests 0 0
        @trainer
        """

        logger.info(f"#parse_trainer: start: url={response.url}")

        # Parse trainer
        logger.debug("#parse_trainer: parse trainer")

        loader = ItemLoader(item=TrainerItem(), response=response)
        loader.add_value("trainer_id", response.url.split("?")[-1])
        loader.add_xpath("trainer_name", "//div[contains(@class,'section')]/div/span[1]/text()")

        table = response.xpath("//table[contains(@class,'tb72')]")[0]

        if table.xpath("tr[1]/th/text()").get() != "生年月日":
            raise RuntimeError("Unknown header birthday")
        else:
            loader.add_value("birthday", table.xpath("tr[1]/td/text()").get())

        if table.xpath("tr[2]/th/text()").get() != "性別":
            raise RuntimeError("Unknown header birthday")
        else:
            loader.add_value("gender", table.xpath("tr[2]/td/text()").get())

        if table.xpath("tr[3]/th/text()").get() != "所属":
            raise RuntimeError("Unknown header birthday")
        else:
            loader.add_value("belong_to", table.xpath("tr[3]/td/text()").get())

        i = loader.load_item()

        logger.info(f"#parse_trainer: trainer={i}")
        yield i
