from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.loader import ItemLoader

from local_horse_racing_crawler.items import RaceInfoItem


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

        # TODO
        # elif url.startswith("https://race.netkeiba.com/race/result.html?race_id="):
        #     self.logger.debug("#_follow: follow race_result page")
        #     return scrapy.Request(url, callback=self.parse_race_result, meta=meta)

        # elif url.startswith("https://db.netkeiba.com/race/"):
        #     self.logger.debug("#_follow: follow old_race_result page")
        #     return scrapy.Request(url, callback=self.parse_old_race_result, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_win_place page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_win_place, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_bracket_quinella page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_bracket_quinella, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_quinella page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_quinella, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_win_quinella_place page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_quinella_place, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_exacta page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_exacta, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_trio page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_trio, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id="):
        #     self.logger.debug("#_follow: follow race_odds_trifecta page")
        #     return scrapy.Request(url, callback=self.parse_race_odds_trifecta, meta=meta)

        # elif url.startswith("https://race.netkeiba.com/race/oikiri.html?race_id="):
        #     self.logger.debug("#_follow: follow training page")
        #     return scrapy.Request(url, callback=self.parse_training, meta=meta)

        # elif url.startswith("https://db.netkeiba.com/v1.1/?pid=api_db_horse_info_simple"):
        #     self.logger.debug("#_follow: follow horse data")
        #     return scrapy.Request(url, callback=self.parse_horse, meta=meta)

        # elif url.startswith("https://db.netkeiba.com/horse/ped/"):
        #     self.logger.debug("#_follow: follow parent_horse page")
        #     return scrapy.Request(url, callback=self.parse_parent_horse, meta=meta)

        # elif url.startswith("https://db.netkeiba.com/jockey/"):
        #     self.logger.debug("#_follow: follow jockey page")
        #     return scrapy.Request(url, callback=self.parse_jockey, meta=meta)

        # elif url.startswith("https://db.netkeiba.com/trainer/"):
        #     self.logger.debug("#_follow: follow trainer page")
        #     return scrapy.Request(url, callback=self.parse_trainer, meta=meta)

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
        @returns items 1 1
        @returns requests 0 0
        @race_program_contract
        """
        self.logger.info(f"#parse_race_program: start: response={response.url}")

        race_program_url = urlparse(response.url)
        race_program_qs = parse_qs(race_program_url.query)

        # Parse race info
        self.logger.debug("#parse_race_program: parse race info")

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

    # TODO
    # def parse_race_result(self, response):
    #     """Parse race_result page.

    #     @url https://race.netkeiba.com/race/result.html?race_id=202306020702
    #     @returns items 27 27
    #     @returns requests 72 72
    #     @race_result_contract
    #     """
    #     self.logger.info(f"#parse_race_result: start: response={response.url}")

    #     race_result_url = urlparse(response.url)
    #     race_result_url_qs = parse_qs(race_result_url.query)

    #     # Parse race info
    #     self.logger.debug("#parse_race_result: parse race info")

    #     loader = ItemLoader(item=RaceInfoItem(type="RaceInfoItem"), response=response)
    #     loader.add_value("race_id", race_result_url_qs["race_id"])
    #     loader.add_xpath("race_round", "string(//span[@class='RaceNum'])")
    #     loader.add_xpath("race_name", "string(//div[@class='RaceName'])")
    #     loader.add_xpath("race_data1", "string(//div[@class='RaceData01'])")
    #     loader.add_xpath("race_data2", "string(//div[@class='RaceData02'])")
    #     loader.add_xpath("race_data3", "//title/text()")
    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_race_result: race_info={i}")
    #     yield i

    #     # Parse race result
    #     self.logger.debug("#parse_race_result: parse race result")

    #     tr = response.xpath("//table[@id='All_Result_Table']/thead/tr[@class='Header']")
    #     assert tr.xpath("string(th[1])").extract_first() == "着順", tr.xpath("string(th[1])").extract_first()
    #     assert tr.xpath("string(th[2])").extract_first() == "枠", tr.xpath("string(th[2])").extract_first()
    #     assert tr.xpath("string(th[3])").extract_first() == "馬番", tr.xpath("string(th[3])").extract_first()
    #     assert tr.xpath("string(th[4])").extract_first().strip() == "馬名", tr.xpath("string(th[4])").extract_first()
    #     assert tr.xpath("string(th[5])").extract_first() == "性齢", tr.xpath("string(th[5])").extract_first()
    #     assert tr.xpath("string(th[6])").extract_first() == "斤量", tr.xpath("string(th[6])").extract_first()
    #     assert tr.xpath("string(th[7])").extract_first() == "騎手", tr.xpath("string(th[7])").extract_first()
    #     assert tr.xpath("string(th[8])").extract_first() == "タイム", tr.xpath("string(th[8])").extract_first()
    #     assert tr.xpath("string(th[9])").extract_first() == "着差", tr.xpath("string(th[9])").extract_first()
    #     assert tr.xpath("string(th[10])").extract_first() == "人気", tr.xpath("string(th[10])").extract_first()
    #     assert tr.xpath("string(th[11])").extract_first() == "単勝オッズ", tr.xpath("string(th[11])").extract_first()
    #     assert tr.xpath("string(th[12])").extract_first() == "後3F", tr.xpath("string(th[12])").extract_first()
    #     assert tr.xpath("string(th[13])").extract_first() == "コーナー通過順", tr.xpath("string(th[13])").extract_first()
    #     assert tr.xpath("string(th[14])").extract_first() == "厩舎", tr.xpath("string(th[14])").extract_first()
    #     assert tr.xpath("string(th[15])").extract_first() == "馬体重(増減)", tr.xpath("string(th[15])").extract_first()

    #     horse_number = 0
    #     for tr in response.xpath("//table[@id='All_Result_Table']/tbody/tr"):
    #         loader = ItemLoader(item=RaceResultItem(type="RaceResultItem"), selector=tr)
    #         loader.add_value("race_id", race_result_url_qs["race_id"])
    #         loader.add_xpath("result", "string(td[1])")
    #         loader.add_xpath("bracket_number", "string(td[2])")
    #         loader.add_xpath("horse_number", "string(td[3])")
    #         loader.add_xpath("horse_id_url", "td[4]/span/a/@href")
    #         loader.add_xpath("jockey_weight", "string(td[6])")
    #         loader.add_xpath("jockey_id_url", "td[7]/a/@href")
    #         loader.add_xpath("arrival_time", "string(td[8])")
    #         loader.add_xpath("arrival_margin", "string(td[9])")
    #         loader.add_xpath("favorite_order", "string(td[10])")
    #         loader.add_xpath("final_600_meters_time", "string(td[12])")
    #         loader.add_xpath("corner_passing_order", "string(td[13])")
    #         loader.add_xpath("trainer_id_url", "td[14]/a/@href")
    #         loader.add_xpath("horse_weight_and_diff", "string(td[15])")
    #         i = loader.load_item()

    #         self.logger.debug(f"#parse_race_result: race_result={i}")
    #         yield i

    #         horse_number += 1

    #     # Parse race payoff
    #     self.logger.debug("#parse_race_result: parse race payoff")

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Tansho']")
    #     loader = ItemLoader(item=RacePayoffItem(type="RacePayoffItem"), selector=tr)
    #     loader.add_value("race_id", race_result_url_qs["race_id"])
    #     loader.add_xpath("betting_type", "th/text()")
    #     loader.add_xpath("horse_numbers", "td[@class='Result']/div[1]/span/text()")
    #     loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
    #     i = loader.load_item()
    #     assert i["betting_type"][0] == "単勝", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Fukusho']")
    #     loader = ItemLoader(item=RacePayoffItem(type="RacePayoffItem"), selector=tr)
    #     loader.add_value("race_id", race_result_url_qs["race_id"])
    #     loader.add_xpath("betting_type", "th/text()")
    #     loader.add_xpath("horse_numbers", "td[@class='Result']/div/span/text()")
    #     loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
    #     i = loader.load_item()
    #     assert i["betting_type"][0] == "複勝", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     def load_item_ren(tr):
    #         loader = ItemLoader(item=RacePayoffItem(type="RacePayoffItem"), selector=tr)
    #         loader.add_value("race_id", race_result_url_qs["race_id"])
    #         loader.add_xpath("betting_type", "th/text()")
    #         loader.add_xpath("horse_numbers", "td[@class='Result']/ul/li/span/text()")
    #         loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
    #         return loader.load_item()

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Wakuren']")
    #     if tr:
    #         # NOTE: 枠連は存在しないことがある
    #         i = load_item_ren(tr)
    #         assert i["betting_type"][0] == "枠連", i["betting_type"][0]

    #         self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #         yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Umaren']")
    #     i = load_item_ren(tr)
    #     assert i["betting_type"][0] == "馬連", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Wide']")
    #     i = load_item_ren(tr)
    #     assert i["betting_type"][0] == "ワイド", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Umatan']")
    #     i = load_item_ren(tr)
    #     assert i["betting_type"][0] == "馬単", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Fuku3']")
    #     i = load_item_ren(tr)
    #     assert i["betting_type"][0] == "3連複", i["betting_type"][0]

    #     self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #     yield i

    #     tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Tan3']")
    #     if tr:
    #         i = load_item_ren(tr)
    #         assert i["betting_type"][0] == "3連単", i["betting_type"][0]

    #         self.logger.debug(f"#parse_race_result: race_payoff={i}")
    #         yield i
    #     else:
    #         self.logger.debug("#parse_race_result: race_payoff not found: Tan3")

    #     # Parse corner passing
    #     tbody = response.xpath("//table[contains(@class, 'Corner_Num')]/tbody")
    #     loader = ItemLoader(item=RaceCornerPassingItem(type="RaceCornerPassingItem"), selector=tbody)
    #     loader.add_value("race_id", race_result_url_qs["race_id"])
    #     loader.add_xpath("corner_name", "tr/th")
    #     loader.add_xpath("passing_order", "tr/td")
    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_race_result: race_corner_passing={i}")
    #     yield i

    #     # Parse lap time
    #     tbody = response.xpath("//table[contains(@class, 'Race_HaronTime')]/tbody")
    #     loader = ItemLoader(item=RaceLapTimeItem(type="RaceLapTimeItem"), selector=tbody)
    #     loader.add_value("race_id", race_result_url_qs["race_id"])
    #     loader.add_xpath("length", "tr[1]/th/text()")
    #     loader.add_xpath("time1", "tr[2]/td/text()")
    #     loader.add_xpath("time2", "tr[3]/td/text()")
    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_race_result: race_lap_time={i}")
    #     yield i

    #     # Parse link
    #     self.logger.debug("#parse_race_result: parse link")

    #     for a in response.xpath("//a"):
    #         url = urlparse(response.urljoin(a.xpath("@href").get()))
    #         url_qs = parse_qs(url.query)

    #         if url.hostname == "race.netkeiba.com" and url.path == "/odds/index.html" and "race_id" in url_qs:
    #             self.logger.debug(f"#parse_race_result: odds top page link. a={url.geturl()}")

    #             # 単勝・複勝
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # 枠連
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # 馬連
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # ワイド
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # 馬単
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # 3連複
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #             # 3連単
    #             race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_odds_url)

    #         elif url.hostname == "race.netkeiba.com" and url.path == "/race/oikiri.html" and "race_id" in url_qs:
    #             self.logger.debug(f"#parse_race_result: training page link. a={url.geturl()}")

    #             race_training_url = f"https://race.netkeiba.com/race/oikiri.html?race_id={url_qs['race_id'][0]}"
    #             yield self._follow(race_training_url)

    #         elif url.hostname == "db.netkeiba.com" and url.path.startswith("/horse/"):
    #             self.logger.debug(f"#parse_race_result: horse page link. a={url.geturl()}")

    #             horse_id_re = re.match("^/horse/(\\w+)/?$", url.path)
    #             horse_url = f"https://db.netkeiba.com/v1.1/?pid=api_db_horse_info_simple&input=UTF-8&output=json&id={horse_id_re.group(1)}"

    #             yield self._follow(horse_url)

    #             parent_horse_url = f"https://db.netkeiba.com/horse/ped/{horse_id_re.group(1)}/"

    #             yield self._follow(parent_horse_url)

    #         elif url.hostname == "db.netkeiba.com" and url.path.startswith("/jockey/result/recent/"):
    #             self.logger.debug(f"#parse_race_result: jockey page link. a={url.geturl()}")

    #             if url.path.startswith("/jockey/result/recent//"):
    #                 # NOTE: 騎手IDが存在しない場合がある、何故か
    #                 self.logger.debug("#parse_race_result: skip")
    #                 continue

    #             jockey_id_re = re.match("^/jockey/result/recent/(\\w+)/?$", url.path)
    #             jockey_url = f"https://db.netkeiba.com/jockey/{jockey_id_re.group(1)}"

    #             yield self._follow(jockey_url)

    #         elif url.hostname == "db.netkeiba.com" and url.path.startswith("/trainer/result/recent/"):
    #             self.logger.debug(f"#parse_race_result: trainer page link. a={url.geturl()}")

    #             if url.path.startswith("/trainer/result/recent//"):
    #                 # NOTE: 調教師IDが存在しない場合がある、何故か
    #                 self.logger.debug("#parse_race_result: skip")
    #                 continue

    #             trainer_id_re = re.match("^/trainer/result/recent/(\\w+)/?$", url.path)
    #             trainer_url = f"https://db.netkeiba.com/trainer/{trainer_id_re.group(1)}"

    #             yield self._follow(trainer_url)

    # def parse_race_odds_win_place(self, response):
    #     """Parse odds_win_place page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id=202306020702
    #     @returns items 32 32
    #     @returns requests 0 0
    #     @odds_win_place_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_win_place: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse win odds
    #     for horse_number, odds in json_odds["data"]["odds"]["1"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 1)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_win_place: odds={item}")
    #         yield item

    #     # Parse place odds
    #     for horse_number, odds in json_odds["data"]["odds"]["2"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 2)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_win_place: odds={item}")
    #         yield item

    # def parse_old_race_result(self, response):
    #     """Parse old_race_result page.

    #     @url https://db.netkeiba.com/race/198606020301/
    #     """
    #     self.logger.info(f"#parse_old_race_result: start: response={response.url}")

    # def parse_race_odds_bracket_quinella(self, response):
    #     """Parse odds_bracket_quinella page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id=202306020702
    #     # 枠連が無い @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id=202304010304
    #     @returns items 36 36
    #     @returns requests 0 0
    #     @odds_bracket_quinella_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_bracket_quinella: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse bracket_quinella odds
    #     for horse_number, odds in json_odds["data"]["odds"]["3"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 3)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_bracket_quinella: odds={item}")
    #         yield item

    # def parse_race_odds_quinella(self, response):
    #     """Parse odds_quinella page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id=202306020702
    #     @returns items 120 120
    #     @returns requests 0 0
    #     @odds_quinella_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_quinella: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse quinella odds
    #     for horse_number, odds in json_odds["data"]["odds"]["4"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 4)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_quinella: odds={item}")
    #         yield item

    # def parse_race_odds_quinella_place(self, response):
    #     """Parse odds_quinella_place page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id=202306020702
    #     @returns items 120 120
    #     @returns requests 0 0
    #     @odds_quinella_place_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_quinella_place: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse quinella_place odds
    #     for horse_number, odds in json_odds["data"]["odds"]["5"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 5)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_quinella_place: odds={item}")
    #         yield item

    # def parse_race_odds_exacta(self, response):
    #     """Parse odds_exacta page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id=202306020702
    #     @returns items 240 240
    #     @returns requests 0 0
    #     @odds_exacta_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_exacta: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse exacta odds
    #     for horse_number, odds in json_odds["data"]["odds"]["6"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 6)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_exacta: odds={item}")
    #         yield item

    # def parse_race_odds_trio(self, response):
    #     """Parse odds_trio page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id=202306020702
    #     @returns items 560 560
    #     @returns requests 0 0
    #     @odds_trio_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_trio: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse trio odds
    #     for horse_number, odds in json_odds["data"]["odds"]["7"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 7)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_trio: odds={item}")
    #         yield item

    # def parse_race_odds_trifecta(self, response):
    #     """Parse odds_trifecta page.

    #     @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id=202306020702
    #     @returns items 3360 3360
    #     @returns requests 0 0
    #     @odds_trifecta_contract
    #     """
    #     self.logger.info(f"#parse_race_odds_trifecta: start: response={response.url}")

    #     odds_url = urlparse(response.url)
    #     odds_qs = parse_qs(odds_url.query)

    #     # Assertion
    #     json_odds = json.loads(response.text)

    #     if json_odds["status"] == "middle":
    #         # NOTE: オッズが無い場合
    #         return

    #     assert json_odds["status"] == "result"
    #     assert json_odds["data"]["official_datetime"] is not None

    #     # Parse trifecta odds
    #     for horse_number, odds in json_odds["data"]["odds"]["8"].items():
    #         loader = ItemLoader(item=OddsItem(type="OddsItem"))
    #         loader.add_value("race_id", odds_qs["race_id"])
    #         loader.add_value("odds_type", 8)
    #         loader.add_value("horse_number", horse_number)
    #         loader.add_value("odds1", odds[0])
    #         loader.add_value("odds2", odds[1])
    #         loader.add_value("favorite_order", odds[2])
    #         item = loader.load_item()

    #         self.logger.debug(f"#parse_race_odds_trifecta: odds={item}")
    #         yield item

    # def parse_training(self, response):
    #     """Parse training page.

    #     @url https://race.netkeiba.com/race/oikiri.html?race_id=202306020702
    #     @returns items 16 16
    #     @returns requests 0 0
    #     @training_contract
    #     """
    #     self.logger.info(f"#parse_training: start: response={response.url}")

    #     training_url = urlparse(response.url)
    #     training_url_qs = parse_qs(training_url.query)

    #     # Parse training
    #     for i, tr in enumerate(response.xpath("//table[@id='All_Oikiri_Table']/tr")):
    #         if i == 0:
    #             assert tr.xpath("string(th[1])").extract_first() == "枠", tr.xpath("string(th[1])").extract_first()
    #             assert tr.xpath("string(th[2])").extract_first() == "馬番", tr.xpath("string(th[2])").extract_first()
    #             assert tr.xpath("string(th[3])").extract_first().strip() == "印", tr.xpath("string(th[3])").extract_first()
    #             assert tr.xpath("string(th[4])").extract_first() == "馬名", tr.xpath("string(th[4])").extract_first()
    #             assert tr.xpath("string(th[5])").extract_first() == "評価", tr.xpath("string(th[5])").extract_first()

    #         else:
    #             loader = ItemLoader(item=TrainingItem(type="TrainingItem"), selector=tr)
    #             loader.add_value("race_id", training_url_qs["race_id"])
    #             loader.add_xpath("horse_number", "string(td[1])")
    #             loader.add_xpath("horse_id_url", "td[4]/div[@class='Horse_Name']/a/@href")
    #             loader.add_xpath("evaluation_text", "string(td[5])")
    #             loader.add_xpath("evaluation_rank", "string(td[6])")
    #             i = loader.load_item()

    #             self.logger.debug(f"#parse_training: training={i}")
    #             yield i

    # def parse_horse(self, response):
    #     """Parse horse data.

    #     @url https://db.netkeiba.com/v1.1/?pid=api_db_horse_info_simple&input=UTF-8&output=json&id=2020100583
    #     @returns items 1 1
    #     @returns requests 0 0
    #     @horse_contract
    #     """
    #     self.logger.info(f"#parse_horse: start: response={response.url}")

    #     horse_url = urlparse(response.url)
    #     horse_qs = parse_qs(horse_url.query)

    #     # Assertion
    #     json_horse = json.loads(response.text)

    #     assert json_horse["status"] == "OK"
    #     if "Bamei" in json_horse["data"]["Horse"]:
    #         json_horse_data = json_horse["data"]["Horse"]
    #     elif "Bamei" in json_horse["data"]["info"]["latest"]:
    #         json_horse_data = json_horse["data"]["info"]["latest"]
    #     else:
    #         raise Exception("Horse data not found")

    #     # Parse horse
    #     loader = ItemLoader(item=HorseItem(type="HorseItem"))
    #     loader.add_value("horse_id", horse_qs["id"][0])
    #     loader.add_value("horse_name", json_horse_data["Bamei"])
    #     loader.add_value("gender", json_horse_data["SexCD"])
    #     loader.add_value("birthday", json_horse_data["BirthDate"] if "BirthDate" in json_horse_data else "")
    #     loader.add_value("coat_color", json_horse_data["KeiroCD"] if "KeiroCD" in json_horse_data else "")
    #     loader.add_value("kigo", json_horse_data["UmaKigoCD"] if "UmaKigoCD" in json_horse_data else "")
    #     loader.add_value("tozai", json_horse_data["TozaiCD"] if "TozaiCD" in json_horse_data else "")
    #     loader.add_value("farm", json_horse_data["SanchiName"] if "SanchiName" in json_horse_data else "")
    #     loader.add_value("seri_name", json_horse_data["SeriName"] if "SeriName" in json_horse_data else "")
    #     loader.add_value("seri_price", json_horse_data["SeriPrice"] if "SeriPrice" in json_horse_data else "")
    #     loader.add_value("trainer_id", json_horse_data["ChokyosiCode"])
    #     loader.add_value("breeder_id", json_horse_data["BreederCode"] if "BreederCode" in json_horse_data else "")
    #     loader.add_value("owner_id", json_horse_data["BanusiCode"] if "BanusiCode" in json_horse_data else "")
    #     item = loader.load_item()

    #     self.logger.debug(f"#parse_horse: horse={item}")
    #     yield item

    # def parse_parent_horse(self, response):
    #     """Parse parent_horse page.

    #     @url https://db.netkeiba.com/horse/ped/2020100583/
    #     # https://db.netkeiba.com/horse/ped/000a00c61c/
    #     @returns items 1 1
    #     @returns requests 0 0
    #     @parent_horse_contract
    #     """
    #     self.logger.info(f"#parse_parent_horse: start: response={response.url}")

    #     parent_horse_url = urlparse(response.url)

    #     loader = ItemLoader(item=ParentHorseItem(type="ParentHorseItem"), selector=response.xpath("//table[contains(@class, 'blood_table')]"))
    #     loader.add_value("parent_horse_id", parent_horse_url.path)

    #     loader.add_xpath("parent1_id", "tr[1]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent2_id", "tr[1]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent3_id", "tr[1]/td[3]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[1]/td[4]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[1]/td[5]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[2]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[3]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[3]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[4]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent3_id", "tr[5]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[5]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[5]/td[3]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[6]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[7]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[7]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[8]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent2_id", "tr[9]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent3_id", "tr[9]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[9]/td[3]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[9]/td[4]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[10]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[11]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[11]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[12]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent3_id", "tr[13]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[13]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[13]/td[3]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[14]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[15]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[15]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[16]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent1_id", "tr[17]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent2_id", "tr[17]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent3_id", "tr[17]/td[3]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[17]/td[4]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[17]/td[5]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[18]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[19]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[19]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[20]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent3_id", "tr[21]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[21]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[21]/td[3]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[22]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[23]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[23]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[24]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent2_id", "tr[25]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent3_id", "tr[25]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[25]/td[3]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[25]/td[4]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[26]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[27]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[27]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[28]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent3_id", "tr[29]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent4_id", "tr[29]/td[2]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[29]/td[3]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[30]/td[1]/a[1]/@href")

    #     loader.add_xpath("parent4_id", "tr[31]/td[1]/a[1]/@href")
    #     loader.add_xpath("parent5_id", "tr[31]/td[2]/a[1]/@href")

    #     loader.add_xpath("parent5_id", "tr[32]/td[1]/a[1]/@href")

    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_parent_horse: parent_horse={i}")
    #     yield i

    # def parse_jockey(self, response):
    #     """Parse jockey page.

    #     @url https://db.netkeiba.com/jockey/01075/
    #     @returns items 1 1
    #     @returns requests 0 0
    #     @jockey_contract
    #     """
    #     self.logger.info(f"#parse_jockey: start: response={response.url}")

    #     jockey_url = urlparse(response.url)

    #     loader = ItemLoader(item=JockeyItem(type="JockeyItem"), response=response)
    #     loader.add_value("jockey_id", jockey_url.path)
    #     loader.add_xpath("jockey_name", "//div[@class='Name']/h1/text()")
    #     loader.add_xpath("jockey_text", "//div[@class='Name']/p/text()")

    #     for tr in response.xpath("//table[@id='DetailTable']/tbody/tr"):
    #         if tr.xpath("th/text()").extract_first() == "出身地":
    #             loader.add_value("birth_place", tr.xpath("td/text()").extract_first())

    #         elif tr.xpath("th/text()").extract_first() == "デビュー年":
    #             loader.add_value("debut_year", tr.xpath("td/text()").extract_first())

    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_jockey: jockey={i}")
    #     yield i

    # def parse_trainer(self, response):
    #     """Parse trainer page.

    #     @url https://db.netkeiba.com/trainer/01027/
    #     @returns items 1 1
    #     @returns requests 0 0
    #     @trainer_contract
    #     """
    #     self.logger.info(f"#parse_trainer: start: response={response.url}")

    #     trainer_url = urlparse(response.url)

    #     loader = ItemLoader(item=TrainerItem(type="TrainerItem"), response=response)
    #     loader.add_value("trainer_id", trainer_url.path)
    #     loader.add_xpath("trainer_name", "//div[@class='Name']/h1/text()")
    #     loader.add_xpath("trainer_text", "//div[@class='Name']/p/text()")

    #     for tr in response.xpath("//table[@id='DetailTable']/tbody/tr"):
    #         if tr.xpath("th/text()").extract_first() == "出身地":
    #             loader.add_value("birth_place", tr.xpath("td/text()").extract_first())

    #         elif tr.xpath("th/text()").extract_first() == "デビュー年":
    #             loader.add_value("debut_year", tr.xpath("td/text()").extract_first())

    #     i = loader.load_item()

    #     self.logger.debug(f"#parse_trainer: trainer={i}")
    #     yield i
