from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.loader import ItemLoader

from local_horse_racing_crawler.items import RaceInfoItem, RaceBracketItem


class NetkeibaSpider(scrapy.Spider):
    name = "netkeiba_spider"
    allowed_domains = ["nar.netkeiba.com", "db.netkeiba.com"]

    def __init__(self, start_url="https://nar.netkeiba.com/top/calendar.html?year=2023&month=11", *args, **kwargs):
        super(NetkeibaSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_url]

    def start_requests(self):
        for url in self.start_urls:
            yield self._follow(url)

    def parse(self, response):
        self.logger.info(f"#parse: start: response={response.url}")

        yield self._follow(self.start_urls[0])

    def _follow(self, url):
        self.logger.debug(f"#_follow: start: url={url}")

        # Setting http proxy
        meta = {}
        if self.settings["CRAWL_HTTP_PROXY"]:
            meta["proxy"] = self.settings["CRAWL_HTTP_PROXY"]
        self.logger.debug(f"#_follow: start: meta={meta}")

        # Build request
        if url.startswith("https://nar.netkeiba.com/top/calendar.html?"):
            self.logger.debug("#_follow: follow calendar page")
            return scrapy.Request(url, callback=self.parse_calendar, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date="):
            self.logger.debug("#_follow: follow race_list page")
            return scrapy.Request(url, callback=self.parse_race_list, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/race/shutuba.html?race_id="):
            self.logger.debug("#_follow: follow race_program page")
            return scrapy.Request(url, callback=self.parse_race_program, meta=meta)

        elif url.startswith("https://db.netkeiba.com/horse/"):
            self.logger.debug("#_follow: follow horse page")
            return scrapy.Request(url, callback=self.parse_horse, meta=meta)

        elif url.startswith("https://db.netkeiba.com/jockey/"):
            self.logger.debug("#_follow: follow jockey page")
            return scrapy.Request(url, callback=self.parse_jockey, meta=meta)

        elif url.startswith("https://db.netkeiba.com/trainer/"):
            self.logger.debug("#_follow: follow trainer page")
            return scrapy.Request(url, callback=self.parse_trainer, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id="):
            self.logger.debug("#_follow: follow odds_win_place page")
            return scrapy.Request(url, callback=self.parse_odds_win_place, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id="):
            self.logger.debug("#_follow: follow odds_exacta page")
            return scrapy.Request(url, callback=self.parse_odds_exacta, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id="):
            self.logger.debug("#_follow: follow odds_quinella page")
            return scrapy.Request(url, callback=self.parse_odds_quinella, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id="):
            self.logger.debug("#_follow: follow odds_quinella_place page")
            return scrapy.Request(url, callback=self.parse_odds_quinella_place, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id="):
            self.logger.debug("#_follow: follow odds_trifecta page")
            return scrapy.Request(url, callback=self.parse_odds_trifecta, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id="):
            self.logger.debug("#_follow: follow odds_trio page")
            return scrapy.Request(url, callback=self.parse_odds_trio, meta=meta)

        elif url.startswith("https://nar.netkeiba.com/race/result.html?race_id="):
            self.logger.debug("#_follow: follow race_result page")
            return scrapy.Request(url, callback=self.parse_race_result, meta=meta)

        else:
            raise Exception("Unknown url")

    def parse_calendar(self, response):
        """Parse calendar page.

        @url https://nar.netkeiba.com/top/calendar.html?year=2023&month=11
        @returns items 0 0
        @returns requests 112 112
        @calendar_contract
        """
        self.logger.info(f"#parse_calendar: start: response={response.url}")

        # Parse link
        for a in response.xpath("//table[@class='Calendar_Table']//a"):
            url = urlparse(response.urljoin(a.xpath("@href").get()))
            qs = parse_qs(url.query)

            if url.hostname == "nar.netkeiba.com" and url.path == "/top/race_list.html" and "kaisai_date" in qs and "kaisai_id" in qs:
                self.logger.debug(f"#parse_calendar: a={url.geturl()}")

                follow_url = f"https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={qs['kaisai_date']}"
                yield self._follow(follow_url)

    def parse_race_list(self, response):
        """Parse race_list page.

        @url https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date=20231114
        @returns items 0 0
        @returns requests 58 58
        @race_list_contract
        """
        self.logger.info(f"#parse_race_list: start: response={response.url}")

        # Parse link
        for a in response.xpath("//li[contains(@class, 'RaceList_DataItem')]//a"):
            url = urlparse(response.urljoin(a.xpath("@href").get()))
            qs = parse_qs(url.query)

            if url.hostname == "nar.netkeiba.com" and (url.path == "/race/result.html" or url.path == "/race/shutuba.html") and "race_id" in qs:
                self.logger.debug(f"#parse_race_list: a={url.geturl()}")

                follow_url = f"https://nar.netkeiba.com/race/shutuba.html?race_id={qs['race_id']}"
                yield self._follow(follow_url)

    def parse_race_program(self, response):
        """Parse race_program page.

        @url https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410
        @returns items 17 17
        @returns requests 55 55
        @race_program_contract
        """
        self.logger.info(f"#parse_race_program: start: response={response.url}")

        race_program_url = urlparse(response.url)
        race_program_qs = parse_qs(race_program_url.query)

        #
        self.logger.debug("#parse_race_program: parse race info")
        #

        loader = ItemLoader(item=RaceInfoItem(), response=response)
        loader.add_value("url", response.url + "#race_info")
        loader.add_value("race_id", race_program_qs["race_id"])
        loader.add_xpath("race_round", "normalize-space(//span[@class='RaceNum'])")
        loader.add_xpath("race_name", "normalize-space(//div[@class='RaceName'])")
        loader.add_xpath("race_data1", "normalize-space(//div[@class='RaceData01'])")
        loader.add_xpath("race_data2", "normalize-space(//div[@class='RaceData02'])")
        loader.add_xpath("race_data3", "//title/text()")
        i = loader.load_item()

        self.logger.debug(f"#parse_race_program: race_info={i}")
        yield i

        #
        self.logger.debug("#parse_race_program: parse race bracket")
        #

        for tr in response.xpath("//table[contains(@class, 'ShutubaTable')]//tr[@class='HorseList']"):
            loader = ItemLoader(item=RaceBracketItem(), selector=tr)
            loader.add_value("url", response.url + "#race_bracket")
            loader.add_value("race_id", race_program_qs["race_id"])
            loader.add_xpath("bracket_number", "normalize-space(td[1]/text())")
            loader.add_xpath("horse_number", "normalize-space(td[2]/text())")
            loader.add_xpath("horse_url", "td[4]//a/@href")
            loader.add_xpath("jockey_url", "td[7]//a/@href")
            loader.add_xpath("jockey_weight", "normalize-space(td[6]/text())")
            loader.add_xpath("trainer_url", "td[8]//a/@href")
            loader.add_xpath("horse_weight_diff", "normalize-space(string(td[9]))")
            i = loader.load_item()

            self.logger.debug(f"#parse_race_program: race_bracket={i}")
            yield i

        #
        self.logger.debug("#parse_race_program: parse horse/jockey/trainer link")
        #

        for a in response.xpath("//table[contains(@class, 'ShutubaTable')]//tr[@class='HorseList']//a"):
            url = urlparse(a.xpath("@href").get())

            if url.geturl().startswith("https://db.netkeiba.com/horse/"):
                self.logger.debug(f"#parse_race_program: horse link={url.geturl()}")

                follow_url = url.geturl()

                yield self._follow(follow_url)
            elif url.geturl().startswith("https://db.netkeiba.com/jockey/result/recent/"):
                self.logger.debug(f"#parse_race_program: jockey link={url.geturl()}")

                parts = [p for p in url.geturl().split("/") if len(p) > 0]
                follow_url = f"https://db.netkeiba.com/jockey/{parts[-1]}/"

                yield self._follow(follow_url)
            elif url.geturl().startswith("https://db.netkeiba.com/trainer/result/recent/"):
                self.logger.debug(f"#parse_race_program: trainer link={url.geturl()}")

                parts = [p for p in url.geturl().split("/") if len(p) > 0]
                follow_url = f"https://db.netkeiba.com/trainer/{parts[-1]}/"

                yield self._follow(follow_url)

        #
        self.logger.debug("#parse_race_program: parse odds link")
        #

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_win_place link={follow_url}")
        yield self._follow(follow_url)

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_exacta link={follow_url}")
        yield self._follow(follow_url)

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_quinella link={follow_url}")
        yield self._follow(follow_url)

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_quinella_place link={follow_url}")
        yield self._follow(follow_url)

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_trifecta link={follow_url}")
        yield self._follow(follow_url)

        follow_url = f"https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: odds_trio link={follow_url}")
        yield self._follow(follow_url)

        #
        self.logger.debug("#parse_race_program: parse race result link")
        #

        follow_url = f"https://nar.netkeiba.com/race/result.html?race_id={race_program_qs['race_id']}"
        self.logger.debug(f"#parse_race_program: race_result link={follow_url}")
        yield self._follow(follow_url)

    def parse_horse(self, response):
        """Parse horse page.

        @url https://db.netkeiba.com/horse/2017103463
        @returns items 0 0
        @returns requests 0 0
        @horse_contract
        """
        self.logger.info(f"#parse_horse: start: response={response.url}")

    def parse_jockey(self, response):
        """Parse jockey page.

        @url https://db.netkeiba.com/jockey/05590
        @returns items 0 0
        @returns requests 0 0
        @jockey_contract
        """
        self.logger.info(f"#parse_jockey: start: response={response.url}")

    def parse_trainer(self, response):
        """Parse trainer page.

        @url https://db.netkeiba.com/trainer/05655
        @returns items 0 0
        @returns requests 0 0
        @trainer_contract
        """
        self.logger.info(f"#parse_trainer: start: response={response.url}")

    def parse_odds_win_place(self, response):
        """Parse odds_win_place page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_win_place_contract
        """
        self.logger.info(f"#parse_odds_win_place: start: response={response.url}")

    def parse_odds_exacta(self, response):
        """Parse odds_exacta page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_exacta_contract
        """
        self.logger.info(f"#parse_odds_exacta: start: response={response.url}")

    def parse_odds_quinella(self, response):
        """Parse odds_quinella page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_quinella_contract
        """
        self.logger.info(f"#parse_odds_quinella: start: response={response.url}")

    def parse_odds_quinella_place(self, response):
        """Parse odds_quinella_place page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_quinella_place_contract
        """
        self.logger.info(f"#parse_odds_quinella_place start: response={response.url}")

    def parse_odds_trifecta(self, response):
        """Parse odds_trifecta page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_trifecta_contract
        """
        self.logger.info(f"#parse_odds_trifecta start: response={response.url}")

    def parse_odds_trio(self, response):
        """Parse odds_trio page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @odds_trio_contract
        """
        self.logger.info(f"#parse_odds_trio start: response={response.url}")

    def parse_race_result(self, response):
        """Parse race_result page.

        @url https://nar.netkeiba.com/race/result.html?race_id=202344111410
        @returns items 0 0
        @returns requests 0 0
        @race_result_contract
        """
        self.logger.info(f"#parse_race_result start: response={response.url}")
