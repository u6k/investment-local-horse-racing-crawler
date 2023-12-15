from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.loader import ItemLoader

from local_horse_racing_crawler.items import RaceInfoItem, RaceBracketItem, RaceResultItem, RacePayoffItem, RaceCornerPassingOrderItem, RaceLaptimeItem, HorseItem, ParentHorseItem, JockeyItem, TrainerItem, OddsItem


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

        elif url.startswith("https://db.netkeiba.com/horse/ped/"):
            self.logger.debug("#_follow: follow parent_horse page")
            return scrapy.Request(url, callback=self.parse_parent_horse, meta=meta)

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
        @returns items 1 1
        @returns requests 1 1
        @horse_contract
        """
        self.logger.info(f"#parse_horse: start: response={response.url}")

        parts = [p for p in response.url.split("/") if len(p) > 0]
        horse_id = parts[-1]

        #
        self.logger.debug("#parse_horse: parse horse")
        #

        loader = ItemLoader(item=HorseItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("horse_id", horse_id)
        loader.add_xpath("horse_name", "normalize-space(//div[@class='horse_title']/h1/text())")
        loader.add_xpath("gender_coat_color", "normalize-space(//div[@class='horse_title']/p/text())")

        for tr in response.xpath("//table[contains(@class, 'db_prof_table')]//tr"):
            if tr.xpath("th/text()").get() == "生年月日":
                loader.add_value("birthday", tr.xpath("td/text()").get())

            elif tr.xpath("th/text()").get() == "馬主":
                follow_path = tr.xpath("td/a/@href").get()
                follow_url = urlparse(response.urljoin(follow_path)).geturl()

                loader.add_value("owner_url", follow_url)
                loader.add_value("owner_name", tr.xpath("td/a/text()").get())

            elif tr.xpath("th/text()").get() == "生産者":
                follow_path = tr.xpath("td/a/@href").get()
                follow_url = urlparse(response.urljoin(follow_path)).geturl()

                loader.add_value("breeder_url", follow_url)
                loader.add_value("breeder_name", tr.xpath("td/a/text()").get())

            elif tr.xpath("th/text()").get() == "産地":
                loader.add_value("breeding_farm", tr.xpath("td/text()").get())

        i = loader.load_item()

        self.logger.debug(f"#parse_horse: horse={i}")
        yield i

        #
        self.logger.debug("#parse_horse: parse link")
        #

        follow_url = f"https://db.netkeiba.com/horse/ped/{horse_id}/"
        yield self._follow(follow_url)

    def parse_parent_horse(self, response):
        """Parse parent_horse page.

        @url https://db.netkeiba.com/horse/ped/2017103463/
        @returns items 1 1
        @returns requests 0 0
        @parent_horse_contract
        """
        self.logger.info(f"#parse_parent_horse: start: response={response.url}")

        parts = [p for p in response.url.split("/") if len(p) > 0]
        horse_id = parts[-1]

        loader = ItemLoader(item=ParentHorseItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("horse_id", horse_id)
        loader.add_xpath("parent_horse_url_m", "//table[contains(@class, 'blood_table')]/tr[1]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f", "//table[contains(@class, 'blood_table')]/tr[17]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_m", "//table[contains(@class, 'blood_table')]/tr[1]/td[2]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_f", "//table[contains(@class, 'blood_table')]/tr[9]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_m", "//table[contains(@class, 'blood_table')]/tr[17]/td[2]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_f", "//table[contains(@class, 'blood_table')]/tr[25]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_m_m", "//table[contains(@class, 'blood_table')]/tr[1]/td[3]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_m_f", "//table[contains(@class, 'blood_table')]/tr[5]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_f_m", "//table[contains(@class, 'blood_table')]/tr[9]/td[2]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_f_f", "//table[contains(@class, 'blood_table')]/tr[13]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_m_m", "//table[contains(@class, 'blood_table')]/tr[17]/td[3]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_m_f", "//table[contains(@class, 'blood_table')]/tr[21]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_f_m", "//table[contains(@class, 'blood_table')]/tr[25]/td[2]/a[1]/@href")
        loader.add_xpath("parent_horse_url_f_f_f", "//table[contains(@class, 'blood_table')]/tr[29]/td[1]/a[1]/@href")
        loader.add_xpath("parent_horse_url_m_m_m_m", "//table[contains(@class, 'blood_table')]/tr[1]/td[4]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_m_f", "//table[contains(@class, 'blood_table')]/tr[3]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_m", "//table[contains(@class, 'blood_table')]/tr[5]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_f", "//table[contains(@class, 'blood_table')]/tr[7]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_m", "//table[contains(@class, 'blood_table')]/tr[9]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_f", "//table[contains(@class, 'blood_table')]/tr[11]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_m", "//table[contains(@class, 'blood_table')]/tr[13]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_f", "//table[contains(@class, 'blood_table')]/tr[15]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_m", "//table[contains(@class, 'blood_table')]/tr[17]/td[4]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_f", "//table[contains(@class, 'blood_table')]/tr[19]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_m", "//table[contains(@class, 'blood_table')]/tr[21]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_f", "//table[contains(@class, 'blood_table')]/tr[23]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_m", "//table[contains(@class, 'blood_table')]/tr[25]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_f", "//table[contains(@class, 'blood_table')]/tr[27]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_m", "//table[contains(@class, 'blood_table')]/tr[29]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_f", "//table[contains(@class, 'blood_table')]/tr[31]/td[1]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_m_m_m", "//table[contains(@class, 'blood_table')]/tr[1]/td[5]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_m_m_f", "//table[contains(@class, 'blood_table')]/tr[2]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_m_m_f_m", "//table[contains(@class, 'blood_table')]/tr[3]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_m_f_f", "//table[contains(@class, 'blood_table')]/tr[4]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_m_m", "//table[contains(@class, 'blood_table')]/tr[5]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_m_f", "//table[contains(@class, 'blood_table')]/tr[6]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_f_m", "//table[contains(@class, 'blood_table')]/tr[7]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_m_f_f_f", "//table[contains(@class, 'blood_table')]/tr[8]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_m_m", "//table[contains(@class, 'blood_table')]/tr[9]/td[4]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_m_f", "//table[contains(@class, 'blood_table')]/tr[10]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_f_m", "//table[contains(@class, 'blood_table')]/tr[11]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_m_f_f", "//table[contains(@class, 'blood_table')]/tr[12]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_m_m", "//table[contains(@class, 'blood_table')]/tr[13]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_m_f", "//table[contains(@class, 'blood_table')]/tr[14]/td/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_f_m", "//table[contains(@class, 'blood_table')]/tr[15]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_m_f_f_f_f", "//table[contains(@class, 'blood_table')]/tr[16]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_m_m", "//table[contains(@class, 'blood_table')]/tr[17]/td[5]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_m_f", "//table[contains(@class, 'blood_table')]/tr[18]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_f_m", "//table[contains(@class, 'blood_table')]/tr[19]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_m_f_f", "//table[contains(@class, 'blood_table')]/tr[20]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_m_m", "//table[contains(@class, 'blood_table')]/tr[21]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_m_f", "//table[contains(@class, 'blood_table')]/tr[22]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_f_m", "//table[contains(@class, 'blood_table')]/tr[23]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_m_f_f_f", "//table[contains(@class, 'blood_table')]/tr[24]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_m_m", "//table[contains(@class, 'blood_table')]/tr[25]/td[4]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_m_f", "//table[contains(@class, 'blood_table')]/tr[26]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_f_m", "//table[contains(@class, 'blood_table')]/tr[27]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_m_f_f", "//table[contains(@class, 'blood_table')]/tr[28]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_m_m", "//table[contains(@class, 'blood_table')]/tr[29]/td[3]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_m_f", "//table[contains(@class, 'blood_table')]/tr[30]/td/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_f_m", "//table[contains(@class, 'blood_table')]/tr[31]/td[2]/a/@href")
        loader.add_xpath("parent_horse_url_f_f_f_f_f", "//table[contains(@class, 'blood_table')]/tr[32]/td/a/@href")

        i = loader.load_item()

        self.logger.debug(f"#parse_parent_horse: parent_horse={i}")
        yield i

    def parse_jockey(self, response):
        """Parse jockey page.

        @url https://db.netkeiba.com/jockey/05590
        @returns items 1 1
        @returns requests 0 0
        @jockey_contract
        """
        self.logger.info(f"#parse_jockey: start: response={response.url}")

        parts = [p for p in response.url.split("/") if len(p) > 0]
        jockey_id = parts[-1]

        loader = ItemLoader(item=JockeyItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("jockey_id", jockey_id)
        loader.add_xpath("jockey_name", "normalize-space(string(//div[@class='Name']/h1))")

        for tr in response.xpath("//table[@id='DetailTable']/tbody/tr"):
            if tr.xpath("th/text()").get() == "デビュー年":
                loader.add_value("debut_year", tr.xpath("normalize-space(td/text())").get())

        i = loader.load_item()

        self.logger.debug(f"#parse_jockey: jockey={i}")
        yield i

    def parse_trainer(self, response):
        """Parse trainer page.

        @url https://db.netkeiba.com/trainer/05655
        @returns items 1 1
        @returns requests 0 0
        @trainer_contract
        """
        self.logger.info(f"#parse_trainer: start: response={response.url}")

        parts = [p for p in response.url.split("/") if len(p) > 0]
        trainer_id = parts[-1]

        loader = ItemLoader(item=TrainerItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("trainer_id", trainer_id)
        loader.add_xpath("trainer_name", "normalize-space(string(//div[@class='Name']/h1))")

        for tr in response.xpath("//table[@id='DetailTable']/tbody/tr"):
            if tr.xpath("th/text()").get() == "デビュー年":
                loader.add_value("debut_year", tr.xpath("normalize-space(td/text())").get())

        i = loader.load_item()

        self.logger.debug(f"#parse_trainer: trainer={i}")
        yield i

    def parse_odds_win_place(self, response):
        """Parse odds_win_place page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410
        @returns items 32 32
        @returns requests 0 0
        @odds_win_place_contract
        """
        self.logger.info(f"#parse_odds_win_place: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        #
        self.logger.debug("#parse_odds_win_place: parse odds win")
        #

        for tr in response.xpath("//div[@id='odds_tan_block']/table/tr"):
            if len(tr.xpath("td")) == 0:
                # ヘッダーの場合はスキップ
                continue

            loader = ItemLoader(item=OddsItem(), selector=tr)
            loader.add_value("url", response.url + "#win")
            loader.add_value("race_id", odds_qs["race_id"])
            loader.add_xpath("horse_number_1", "td[2]/text()")
            loader.add_value("horse_number_2", "")
            loader.add_value("horse_number_3", "")
            loader.add_xpath("odds", "normalize-space(string(td[6]))")
            i = loader.load_item()

            self.logger.debug(f"#parse_odds_win_place: odds_win={i}")
            yield i

        #
        self.logger.debug("#parse_odds_win_place: parse odds place")
        #

        for tr in response.xpath("//div[@id='odds_fuku_block']/table/tr"):
            if len(tr.xpath("td")) == 0:
                # ヘッダーの場合はスキップ
                continue

            loader = ItemLoader(item=OddsItem(), selector=tr)
            loader.add_value("url", response.url + "#place")
            loader.add_value("race_id", odds_qs["race_id"])
            loader.add_xpath("horse_number_1", "td[2]/text()")
            loader.add_value("horse_number_2", "")
            loader.add_value("horse_number_3", "")
            loader.add_xpath("odds", "normalize-space(string(td[6]))")
            i = loader.load_item()

            self.logger.debug(f"#parse_odds_win_place: odds_place={i}")
            yield i

    def parse_odds_exacta(self, response):
        """Parse odds_exacta page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410
        @returns items 240 240
        @returns requests 0 0
        @odds_exacta_contract
        """
        self.logger.info(f"#parse_odds_exacta: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        for table in response.xpath("//table[@class='Odds_Table']"):
            horse_number_1 = None

            for tr in table.xpath("tr"):
                if len(tr.xpath("th")) > 0:
                    horse_number_1 = tr.xpath("th/text()").get()
                else:
                    loader = ItemLoader(item=OddsItem(), selector=tr)
                    loader.add_value("url", response.url)
                    loader.add_value("race_id", odds_qs["race_id"])
                    loader.add_value("horse_number_1", horse_number_1)
                    loader.add_xpath("horse_number_2", "normalize-space(string(td[1]))")
                    loader.add_value("horse_number_3", "")
                    loader.add_xpath("odds", "normalize-space(string(td[2]))")
                    i = loader.load_item()

                    self.logger.debug(f"#parse_odds_exacta: odds_exacta={i}")
                    yield i

    def parse_odds_quinella(self, response):
        """Parse odds_quinella page.

        @url https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410
        @returns items 120 120
        @returns requests 0 0
        @odds_quinella_contract
        """
        self.logger.info(f"#parse_odds_quinella: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        for table in response.xpath("//table[@class='Odds_Table']"):
            horse_number_1 = None

            for tr in table.xpath("tr"):
                if len(tr.xpath("th")) > 0:
                    horse_number_1 = tr.xpath("th/text()").get()
                else:
                    loader = ItemLoader(item=OddsItem(), selector=tr)
                    loader.add_value("url", response.url)
                    loader.add_value("race_id", odds_qs["race_id"])
                    loader.add_value("horse_number_1", horse_number_1)
                    loader.add_xpath("horse_number_2", "normalize-space(string(td[1]))")
                    loader.add_value("horse_number_3", "")
                    loader.add_xpath("odds", "normalize-space(string(td[2]))")
                    i = loader.load_item()

                    self.logger.debug(f"#parse_odds_quinella: odds_exacta={i}")
                    yield i

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
        @returns items 30 30
        @returns requests 0 0
        @race_result_contract
        """
        self.logger.info(f"#parse_race_result: start: response={response.url}")

        race_result_url = urlparse(response.url)
        race_result_qs = parse_qs(race_result_url.query)

        #
        self.logger.debug("#parse_race_result: parse race result")
        #

        for tr in response.xpath("//table[contains(@class, 'ResultRefund')]//tr"):
            if len(tr.xpath("td")) == 0:
                # ヘッダーの場合はスキップ
                continue

            loader = ItemLoader(item=RaceResultItem(), selector=tr)
            loader.add_value("url", response.url + "#race_result")
            loader.add_value("race_id", race_result_qs["race_id"])
            loader.add_xpath("result", "normalize-space(string(td[1]))")
            loader.add_xpath("bracket_number", "normalize-space(string(td[2]))")
            loader.add_xpath("horse_number", "normalize-space(string(td[3]))")
            loader.add_xpath("horse_url", "td[4]//a/@href")
            loader.add_xpath("arrival_time", "normalize-space(string(td[8]))")
            loader.add_xpath("arrival_margin", "normalize-space(string(td[9]))")
            loader.add_xpath("final_600_meters_time", "normalize-space(string(td[12]))")
            i = loader.load_item()

            self.logger.debug(f"#parse_race_result: race_result={i}")
            yield i

        #
        self.logger.debug("#parse_race_result: parse race payoff")
        #

        for tr in response.xpath("//table[@class='Payout_Detail_Table']//tr"):
            loader = ItemLoader(item=RacePayoffItem(), selector=tr)
            loader.add_value("url", response.url + "#race_payoff")
            loader.add_value("race_id", race_result_qs["race_id"])
            loader.add_xpath("bet_type", "normalize-space(string(th))")
            loader.add_xpath("horse_number", "normalize-space(string(td[1]))")
            loader.add_xpath("payoff_money", "normalize-space(string(td[2]))")
            loader.add_xpath("favorite_order", "normalize-space(string(td[3]))")
            i = loader.load_item()

            self.logger.debug(f"#parse_race_result: race_payoff={i}")
            yield i

        #
        self.logger.debug("#parse_race_result: parse race corner passing order")
        #

        for tr in response.xpath("//table[contains(@class, 'Corner_Num')]//tr"):
            loader = ItemLoader(item=RaceCornerPassingOrderItem(), selector=tr)
            loader.add_value("url", response.url + "#race_corner_passing_order")
            loader.add_value("race_id", race_result_qs["race_id"])
            loader.add_xpath("corner_name", "normalize-space(string(th))")
            loader.add_xpath("passing_order", "normalize-space(string(td))")
            i = loader.load_item()

            self.logger.debug(f"#parse_race_result: race_corner_passing_order={i}")
            yield i

        #
        self.logger.debug("#parse_race_result: parse race laptime")
        #

        for tr in response.xpath("//table[contains(@class, 'Race_HaronTime')]//tr"):
            loader = ItemLoader(item=RaceLaptimeItem(), selector=tr)
            loader.add_value("url", response.url + "#race_laptime")
            loader.add_value("race_id", race_result_qs["race_id"])

            if len(tr.xpath("th")) > 0:
                loader.add_xpath("data", "th/text()")
            else:
                loader.add_xpath("data", "td/text()")

            i = loader.load_item()

            self.logger.debug(f"#parse_race_result: race_laptime={i}")
            yield i
