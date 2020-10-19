import scrapy
from scrapy.loader import ItemLoader

from investment_local_horse_racing_crawler.scrapy.items import CalendarItem, RaceInfoMiniItem, RaceInfoItem, RaceDenmaItem, RaceResultItem, RaceCornerPassingOrderItem, RaceRefundItem, HorseItem, JockeyItem, TrainerItem, OddsWinPlaceItem, OddsUrlItem
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    def __init__(self, start_url="https://www.oddspark.com/keiba/KaisaiCalendar.do", recache_race=False, recache_horse=False, *args, **kwargs):
        logger.info(f"#__init__: start: start_url={start_url}, recache_race={recache_race}, recache_horse={recache_horse}")
        try:
            super(LocalHorseRacingSpider, self).__init__(*args, **kwargs)

            self.start_urls = [start_url]
            self.recache_race = recache_race
            self.recache_horse = recache_horse
        except Exception:
            logger.exception("#__init__: fail")

    def parse(self, response):
        """ Parse start page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do
        @returns items 0 0
        @returns requests 1 1
        """

        logger.info(f"#parse: start: url={response.url}")
        logger.info(f"#parse: recache_race={self.recache_race}")
        logger.info(f"#parse: recache_horse={self.recache_horse}")

        path = response.url[24:]
        yield self._follow_delegate(response, path)

    def parse_calendar(self, response):
        """ Parse calendar page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do?target=202004
        @returns items 1 1
        @returns requests 77 77
        @calendar
        """

        logger.info(f"#parse_calendar: start: url={response.url}")

        # Build item
        loader = ItemLoader(item=CalendarItem(), response=response)
        loader.add_value("calendar_url", response.url)
        for href in response.xpath("//table[contains(@class,'tbSched')]/tr/td/div/a/@href"):
            loader.add_value("race_list_urls", href.get().replace("RaceRefund", "OneDayRaceList"))
        i = loader.load_item()

        logger.debug(f"#parse_calendar: build calendar item={i}")
        yield i

        # Request
        for race_list_url in i["race_list_urls"]:
            logger.debug(f"#parse_calendar: found one day race list page: url={race_list_url}")
            yield self._follow_delegate(response, race_list_url)

    def parse_one_day_race_list(self, response):
        """ Parse one day race list page.

        @url https://www.oddspark.com/keiba/OneDayRaceList.do?opTrackCd=42&raceDy=20200417&sponsorCd=20
        @returns items 11 11
        @returns requests 11 11
        @one_day_race_list
        """

        logger.info(f"#parse_one_day_race_list: start: url={response.url}")

        for div in response.xpath("//div[@class='pB5']"):
            # Build item
            loader = ItemLoader(item=RaceInfoMiniItem(), selector=div)
            loader.add_value("race_list_url", response.url)
            loader.add_xpath("race_name", "normalize-space(strong/a/text())")
            loader.add_xpath("race_denma_url", "strong/a/@href")
            loader.add_xpath("course_length", "normalize-space(.)")
            loader.add_xpath("start_time", "normalize-space(strong[2]/text())")
            i = loader.load_item()

            logger.debug(f"#parse_one_day_race_list: build race summary mini item={i}")
            yield i

            # Request
            logger.debug(f"#parse_one_day_race_list: found race denma page: url={i['race_denma_url'][0]}")
            yield self._follow_delegate(response, i["race_denma_url"][0])

    def parse_race_denma(self, response):
        """ Parse race denma page.

        @url https://www.oddspark.com/keiba/RaceList.do?raceDy=20200417&opTrackCd=42&raceNb=1&sponsorCd=20
        @returns items 1
        @returns requests 1
        @race_denma
        """

        logger.info(f"#parse_race_denma: start: url={response.url}")

        # Parse race info
        logger.debug("#parse_race_denma: parse race info")

        loader = ItemLoader(item=RaceInfoItem(), response=response)
        loader.add_value("race_denma_url", response.url)
        loader.add_xpath("race_round", "//div[@id='RCdata1']/span/text()")
        loader.add_xpath("race_name", "normalize-space(//div[@id='RCdata2']/h3/text())")
        loader.add_xpath("start_date", "//div[@id='RCdata2']/ul/li[@class='RCdate']/text()")
        loader.add_xpath("place_name", "normalize-space(//div[@id='RCdata2']/ul/li[@class='RCnum']/text())")
        loader.add_xpath("course_type_length", "//div[@id='RCdata2']/ul/li[@class='RCdst']/text()")
        loader.add_xpath("start_time", "//div[@id='RCdata2']/ul/li[@class='RCstm']/text()")
        loader.add_xpath("weather_url", "//div[@id='RCdata2']/ul/li[@class='RCwthr']/img/@src")
        loader.add_xpath("moisture", "//div[@id='RCdata2']/ul/li[@class='RCwatr']/span[@class='baba']/text()")
        loader.add_xpath("course_condition", "//div[@id='RCdata2']/ul/li[@class='RCcnd']/img/@src")
        loader.add_xpath("prize_money", "normalize-space(//div[@id='RCdata2']/p/text())")
        i = loader.load_item()

        logger.info(f"#parse_race_denma: race info={i}")
        yield i

        # Parse race denma
        logger.debug("#parse_race_denma: parse race denma")

        for tr in response.xpath("//table[contains(@class,'ent1')]/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            if len(tr.xpath("td")) == 15:
                bracket_number = tr.xpath("normalize-space(td[1]/text())").get()

                loader = ItemLoader(item=RaceDenmaItem(), selector=tr)
                loader.add_value("race_denma_url", response.url)
                loader.add_value("bracket_number", bracket_number)
                loader.add_xpath("horse_number", "normalize-space(td[3]/text())")
                loader.add_xpath("horse_url", "td[5]/a/@href")
                loader.add_xpath("jockey_url", "td[6]/a[1]/@href")
                loader.add_xpath("jockey_weight", "normalize-space(td[6]/strong/text())")
                loader.add_xpath("trainer_url", "td[6]/a[2]/@href")
                loader.add_xpath("odds_win_favorite", "normalize-space(td[7])")
                loader.add_xpath("horse_weight", "normalize-space(td[8]/text()[1])")
                loader.add_xpath("horse_weight_diff", "normalize-space(td[8]/text()[2])")
                i = loader.load_item()

                logger.debug(f"#parse_race_denma: race denma={i}")
                yield i
            elif len(tr.xpath("td")) == 13:
                loader = ItemLoader(item=RaceDenmaItem(), selector=tr)
                loader.add_value("race_denma_url", response.url)
                loader.add_value("bracket_number", bracket_number)
                loader.add_xpath("horse_number", "normalize-space(td[1]/text())")
                loader.add_xpath("horse_url", "td[3]/a/@href")
                loader.add_xpath("jockey_url", "td[4]/a[1]/@href")
                loader.add_xpath("jockey_weight", "normalize-space(td[4]/strong/text())")
                loader.add_xpath("trainer_url", "td[4]/a[2]/@href")
                loader.add_xpath("odds_win_favorite", "normalize-space(td[5])")
                loader.add_xpath("horse_weight", "normalize-space(td[6]/text()[1])")
                loader.add_xpath("horse_weight_diff", "normalize-space(td[6]/text()[2])")
                i = loader.load_item()

                logger.debug(f"#parse_race_denma: race denma={i}")
                yield i
            else:
                logger.warn("#parse_race_denma: unknown record")

        # Parse link
        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href is None:
                continue

            if href.startswith("/keiba/Odds.do?") \
                    or href.startswith("/keiba/RaceResult.do?") \
                    or href.startswith("/keiba/HorseDetail.do?") \
                    or href.startswith("/keiba/JockeyDetail.do?") \
                    or href.startswith("/keiba/TrainerDetail.do?"):
                yield self._follow_delegate(response, href)

    def parse_race_result(self, response):
        """ Parse race result page.

        @url https://www.oddspark.com/keiba/RaceResult.do?sponsorCd=29&raceDy=20200301&opTrackCd=55&raceNb=10
        @returns items 1
        @returns requests 0 0
        @race_result
        """

        logger.info(f"#parse_race_result: start: url={response.url}")

        # Parse race result
        logger.debug("#parse_race_result: parse race result")

        for tr in response.xpath("//table[@summary='レース結果']/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            loader = ItemLoader(item=RaceResultItem(), selector=tr)
            loader.add_value("race_result_url", response.url)
            loader.add_xpath("result", "td[1]/text()")
            loader.add_xpath("bracket_number", "td[2]/text()")
            loader.add_xpath("horse_number", "td[3]/text()")
            loader.add_xpath("horse_url", "td[4]/a/@href")
            loader.add_xpath("arrival_time", "td[11]/text()")

            if len(tr.xpath("td")) == 15:
                loader.add_xpath("arrival_margin", "td[12]/text()")
                loader.add_xpath("final_600_meters_time", "td[13]/text()")
                loader.add_xpath("corner_passing_order", "td[14]/text()")

            i = loader.load_item()

            logger.debug(f"#parse_race_result: race result={i}")
            yield i

        # Parse race corner passing order
        logger.debug("#parse_race_result: parse race corner passing order")

        for tr in response.xpath("//table[@summary='コーナー通過順']/tr"):
            loader = ItemLoader(item=RaceCornerPassingOrderItem(), selector=tr)
            loader.add_value("race_result_url", response.url)
            loader.add_xpath("corner_number", "normalize-space(th/text())")
            loader.add_xpath("passing_order", "normalize-space(td)")
            i = loader.load_item()

            logger.debug(f"#parse_race_result: race corner passing order item={i}")
            yield i

        # Parse race refund
        logger.debug("#parse_race_result: parse race refund")

        for tr in response.xpath("//table[@summary='払戻金情報']/tr"):
            if len(tr.xpath("th")) > 0:
                betting_type = tr.xpath("th/text()").get()

            loader = ItemLoader(item=RaceRefundItem(), selector=tr)
            loader.add_value("race_result_url", response.url)
            loader.add_value("betting_type", betting_type)
            loader.add_xpath("horse_number", "td[1]/text()")
            loader.add_xpath("refund_money", "td[2]/text()")
            loader.add_xpath("favorite", "td[3]/text()")
            i = loader.load_item()

            logger.debug(f"#parse_race_result: race refund item={i}")
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
        loader.add_value("horse_url", response.url)
        loader.add_xpath("horse_name", "normalize-space(//div[@id='content']/div[2]/span[1]/text())")
        loader.add_xpath("gender_age", "normalize-space(//div[@id='content']/div[2]/span[2]/text())")
        loader.add_xpath("birthday", "normalize-space(//table[contains(@class,'tb72')]/tr[1]/td/text())")
        loader.add_xpath("coat_color", "normalize-space(//table[contains(@class,'tb72')]/tr[2]/td/text())")
        loader.add_xpath("trainer_url", "//table[contains(@class,'tb72')]/tr[3]/td/a/@href")
        loader.add_xpath("owner", "normalize-space(//table[contains(@class,'tb72')]/tr[4]/td/text())")
        loader.add_xpath("breeder", "normalize-space(//table[contains(@class,'tb72')]/tr[5]/td/text())")
        loader.add_xpath("breeding_farm", "normalize-space(//table[contains(@class,'tb72')]/tr[6]/td/text())")
        loader.add_xpath("parent_horse_name_1", "normalize-space(//table[contains(@class,'tb71')]/tr[2]/td[1]/text())")
        loader.add_xpath("parent_horse_name_2", "normalize-space(//table[contains(@class,'tb71')]/tr[4]/td[1]/text())")
        loader.add_xpath("grand_parent_horse_name_1", "normalize-space(//table[contains(@class,'tb71')]/tr[2]/td[2]/text())")
        loader.add_xpath("grand_parent_horse_name_2", "normalize-space(//table[contains(@class,'tb71')]/tr[3]/td[1]/text())")
        loader.add_xpath("grand_parent_horse_name_3", "normalize-space(//table[contains(@class,'tb71')]/tr[4]/td[2]/text())")
        loader.add_xpath("grand_parent_horse_name_4", "normalize-space(//table[contains(@class,'tb71')]/tr[5]/td[1]/text())")
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
        loader.add_value("jockey_url", response.url)
        loader.add_xpath("jockey_name", "normalize-space(//div[@id='content']/div[2]/span[1]/text())")
        loader.add_xpath("birthday", "normalize-space(//table[contains(@class,'tb72')]/tr[1]/td/text())")
        loader.add_xpath("gender", "normalize-space(//table[contains(@class,'tb72')]/tr[2]/td/text())")
        loader.add_xpath("belong_to", "normalize-space(//table[contains(@class,'tb72')]/tr[3]/td/text())")
        loader.add_xpath("trainer_url", "//table[contains(@class,'tb72')]/tr[4]/td/a/@href")
        loader.add_xpath("first_licensing_year", "normalize-space(//table[contains(@class,'tb72')]/tr[5]/td/text())")
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
        loader.add_value("trainer_url", response.url)
        loader.add_xpath("trainer_name", "normalize-space(//div[contains(@class,'section')]/div/span[1]/text())")
        loader.add_xpath("birthday", "normalize-space(//table[contains(@class,'tb72')]/tr[1]/td/text())")
        loader.add_xpath("gender", "normalize-space(//table[contains(@class,'tb72')]/tr[2]/td/text())")
        loader.add_xpath("belong_to", "normalize-space(//table[contains(@class,'tb72')]/tr[3]/td/text())")
        i = loader.load_item()

        logger.info(f"#parse_trainer: trainer={i}")
        yield i

    def parse_odds_win_place(self, response):
        """ Parse odds(win/place) page.

        @url https://www.oddspark.com/keiba/Odds.do?sponsorCd=04&raceDy=20200301&opTrackCd=03&raceNb=1
        @returns items 1
        @returns requests 0 0
        @odds_win_place
        """

        logger.info(f"#parse_odds_win_place: start: url={response.url}")

        # Parse odds win/place
        logger.debug("#parse_odds_win: parse odds win/place")

        for tr in response.xpath("//table[contains(@class,'tb71')]/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            loader = ItemLoader(item=OddsWinPlaceItem(), selector=tr)

            if len(tr.xpath("td")) == 5:
                loader.add_value("odds_url", response.url)
                loader.add_xpath("horse_number", "normalize-space(td[2]/text())")
                loader.add_xpath("horse_url", "td[3]/a/@href")
                loader.add_xpath("odds_win", "normalize-space(td[4]/span/text())")
                loader.add_xpath("odds_place", "normalize-space(td[5])")
            elif len(tr.xpath("td")) == 4:
                loader.add_value("odds_url", response.url)
                loader.add_xpath("horse_number", "normalize-space(td[1]/text())")
                loader.add_xpath("horse_url", "td[2]/a/@href")
                loader.add_xpath("odds_win", "normalize-space(td[3]/span/text())")
                loader.add_xpath("odds_place", "normalize-space(td[4])")
            else:
                logger.warn("Unknown record")
                continue

            i = loader.load_item()

            logger.debug(f"#parse_odds_win: odds win/place={i}")
            yield i

        # Parse odds urls
        logger.debug("#parse_odds_win: parse odds urls")

        loader = ItemLoader(OddsUrlItem(), response=response)
        loader.add_value("odds_url", response.url)

        for a in response.xpath("//div[@id='oddsType']/ul/li/a"):
            href = a.xpath("@href").get()

            if href is not None and href.startswith("/keiba/Odds.do?") and "betType=1" not in href:
                loader.add_value("odds_sub_urls", href)

        i = loader.load_item()

        logger.debug(f"#parse_odds_win: odds urls={i}")
        yield i

        # Request odds urls
        logger.debug("#parse_odds_win: request odds urls")

        for href in i["odds_sub_urls"]:
            yield self._follow_delegate(response, href)

    def _follow_delegate(self, response, path, cb_kwargs=None):
        logger.info(f"#_follow_delegate: start: path={path}, cb_kwargs={cb_kwargs}")

        if path.startswith("/keiba/KaisaiCalendar.do"):
            logger.debug("#_follow_delegate: follow calendar page")
            return response.follow(path, callback=self.parse_calendar, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/OneDayRaceList.do?"):
            logger.debug("#_follow_delegate: follow one day race list page")
            return response.follow(path, callback=self.parse_one_day_race_list, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/RaceList.do?"):
            logger.debug("#_follow_delegate: follow race denma page")
            return response.follow(path, callback=self.parse_race_denma, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/RaceResult.do?"):
            logger.debug("#_follow_delegate: follow race result page")
            return response.follow(path, callback=self.parse_race_result, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/HorseDetail.do?"):
            logger.debug("#_follow_delegate: follow horse page")
            return response.follow(path, callback=self.parse_horse, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/JockeyDetail.do?"):
            logger.debug("#_follow_delegate: follow jockey page")
            return response.follow(path, callback=self.parse_jockey, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/TrainerDetail.do?"):
            logger.debug("#_follow_delegate: follow trainer page")
            return response.follow(path, callback=self.parse_trainer, cb_kwargs=cb_kwargs)

        elif path.startswith("/keiba/Odds.do?") and "betType=6" in path:
            # TODO: 馬連をパースする
            logger.warn("#_follow_delegate: follow odds quinella page")

        elif path.startswith("/keiba/Odds.do?") and "betType=5" in path:
            # TODO: 馬単をパースする
            logger.warn("#_follow_delegate: follow odds exacta page")

        elif path.startswith("/keiba/Odds.do?") and "betType=7" in path:
            # TODO: ワイドをパースする
            logger.warn("#_follow_delegate: follow odds quinella place page")

        elif path.startswith("/keiba/Odds.do?") and "betType=9" in path:
            # TODO: 三連複をパースする
            logger.warn("#_follow_delegate: follow odds trio page")

        elif path.startswith("/keiba/Odds.do?") and "betType=8" in path:
            # TODO: 三連単をパースする
            logger.warn("#_follow_delegate: follow odds trifecta page")

        elif path.startswith("/keiba/Odds.do?"):
            logger.debug("#_follow_delegate: follow odds win/place page")
            return response.follow(path, callback=self.parse_odds_win_place, cb_kwargs=cb_kwargs)

        else:
            logger.warning("#_follow_delegate: unknown path pattern")
