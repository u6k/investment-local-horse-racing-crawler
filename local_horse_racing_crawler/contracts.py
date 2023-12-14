from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

from local_horse_racing_crawler.items import RaceInfoItem, RaceBracketItem, RaceResultItem, RacePayoffItem, RaceCornerPassingOrderItem, RaceLaptimeItem, HorseItem


class CalendarContract(Contract):
    name = "calendar_contract"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        for r in requests:
            if r.url.startswith("https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date="):
                continue

            raise ContractFail("unknown url")


class RaceListContract(Contract):
    name = "race_list_contract"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        for r in requests:
            if r.url.startswith("https://nar.netkeiba.com/race/shutuba.html?race_id="):
                continue

            raise ContractFail("unknown url")


class RaceProgramContract(Contract):
    name = "race_program_contract"

    def post_process(self, output):
        #
        # Check items
        #

        # レース情報
        items = [o for o in output if isinstance(o, RaceInfoItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_info"]
        assert i["race_id"] == ["202344111410"]
        assert i["race_round"] == ["10R"]
        assert i["race_name"] == ["八潮パークタウン40周年特別競走(B2)"]
        assert i["race_data1"] == ["19:30発走 / ダ1200m (右) / 天候:晴 / 馬場:良 \xa0"]
        assert i["race_data2"] == ["13回 大井 2日目 サラ系一般 B2 \xa0\xa0\xa0\xa0\xa0 16頭 本賞金:270.0、108.0、67.5、40.5、27.0万円"]
        assert i["race_data3"] == ["八潮パークタウン40 出馬表 | 2023年11月14日 大井10R 地方競馬レース情報 - netkeiba.com"]

        # 枠データ
        items = [o for o in output if isinstance(o, RaceBracketItem)]

        assert len(items) == 16

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["1"]
        assert i["horse_number"] == ["1"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2017103463"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05590"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05655"]
        assert i["horse_weight_diff"] == ["508(-1)"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["1"]
        assert i["horse_number"] == ["2"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103331"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05554"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05722"]
        assert i["horse_weight_diff"] == ["498(+8)"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["15"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103916"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05443"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05769"]
        assert i["horse_weight_diff"] == ["486(+10)"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["16"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2016101473"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05411"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05655"]
        assert i["horse_weight_diff"] == ["470(+6)"]

        #
        # Check requests
        #

        requests = [o for o in output if isinstance(o, Request)]

        horse_requests = [r for r in requests if r.url.startswith("https://db.netkeiba.com/horse/")]
        assert len(horse_requests) == 16

        jockey_requests = [r for r in requests if r.url.startswith("https://db.netkeiba.com/jockey/")]
        assert len(jockey_requests) == 16

        trainer_requests = [r for r in requests if r.url.startswith("https://db.netkeiba.com/trainer/")]
        assert len(trainer_requests) == 16

        odds_requests = [r for r in requests if r.url.startswith("https://nar.netkeiba.com/odds/odds_get_form.html?")]
        assert len(odds_requests) == 6

        result_requests = [r for r in requests if r.url.startswith("https://nar.netkeiba.com/race/result.html?race_id=")]
        assert len(result_requests) == 1


class HorseContract(Contract):
    name = "horse_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, HorseItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://db.netkeiba.com/horse/2017103463"]
        assert i["horse_id"] == ["2017103463"]
        assert i["horse_name"] == ["ドーロカグラ"]
        assert i["gender_coat_color"] == ["\u3000牡\u3000黒鹿毛"]
        assert i["birthday"] == ["2017年5月9日"]
        assert i["owner_url"] == ["https://db.netkeiba.com/owner/x076d0/"]
        assert i["owner_name"] == ["曽根正"]
        assert i["breeder_url"] == ["https://db.netkeiba.com/breeder/704079/"]
        assert i["breeder_name"] == ["グランド牧場"]
        assert i["breeding_farm"] == ["新ひだか町"]

        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        parent_requests = [r for r in requests if r.url.startswith("https://db.netkeiba.com/horse/ped/")]
        assert len(parent_requests) == 1


class ParentHorseContract(Contract):
    name = "parent_horse_contract"

    def post_process(self, output):
        pass


class JockeyContract(Contract):
    name = "jockey_contract"

    def post_process(self, output):
        pass
#         # Check item
#         items = [o for o in output if isinstance(o, JockeyItem)]

#         if len(items) != 1:
#             raise ContractFail("len(JockeyItem)")

#         item = items[0]

#         jockey_url_re = re.match(r"^https://www\.oddspark\.com/keiba/JockeyDetail\.do\?jkyNb=\d+$", item["jockey_url"][0])
#         if not jockey_url_re:
#             raise ContractFail("jockey_url")

#         if not item["jockey_name"][0]:
#             raise ContractFail("jockey_name")

#         birthday_re = re.match(r"^\d{4}年\d{1,2}月\d{1,2}日$", item["birthday"][0])
#         if not birthday_re:
#             raise ContractFail("birthday")

#         gender_re = re.match(r"^男|女$", item["gender"][0])
#         if not gender_re:
#             raise ContractFail("gender")

#         if not item["belong_to"][0]:
#             raise ContractFail("belong_to")

#         trainer_url_re = re.match(r"^/keiba/TrainerDetail\.do\?trainerNb=\d+$", item["trainer_url"][0])
#         if not trainer_url_re:
#             raise ContractFail("trainer_url")

#         first_licensing_year_re = re.match(r"^\d+年$", item["first_licensing_year"][0])
#         if not first_licensing_year_re:
#             raise ContractFail("first_licensing_year")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("requests is not empty")


class TrainerContract(Contract):
    name = "trainer_contract"

    def post_process(self, output):
        pass
#         # Check item
#         items = [o for o in output if isinstance(o, TrainerItem)]

#         if len(items) != 1:
#             raise ContractFail("len(TrainerItem)")

#         item = items[0]

#         trainer_url_re = re.match(r"https://www\.oddspark\.com/keiba/TrainerDetail\.do\?trainerNb=\d+$", item["trainer_url"][0])
#         if not trainer_url_re:
#             raise ContractFail("trainer_url")

#         if not item["trainer_name"][0]:
#             raise ContractFail("trainer_name")

#         birthday_re = re.match(r"^\d{4}年\d{1,2}月\d{1,2}日$", item["birthday"][0])
#         if not birthday_re:
#             raise ContractFail("birthday")

#         gender_re = re.match(r"^男|女$", item["gender"][0])
#         if not gender_re:
#             raise ContractFail("gender")

#         if not item["belong_to"][0]:
#             raise ContractFail("belong_to")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("requests is not empty")


class OddsWinPlaceContract(Contract):
    name = "odds_win_place_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsWinPlaceItem
#         items = [o for o in output if isinstance(o, OddsWinPlaceItem)]

#         if len(items) == 0:
#             raise ContractFail("len(OddsWinPlaceItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=1.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_re = re.match(r"^\d+$", item["horse_number"][0])
#             if not horse_number_re:
#                 raise ContractFail("horse_number")

#             horse_url_re = re.match(r"/keiba/HorseDetail\.do\?lineageNb=\d+$", item["horse_url"][0])
#             if not horse_url_re:
#                 raise ContractFail("horse_url")

#             odds_win_re = re.match(r"^\d+\.\d+$", item["odds_win"][0])
#             if not odds_win_re:
#                 raise ContractFail("odds_win")

#             odds_place_re = re.match(r"^\d+\.\d+ - \d+\.\d+$", item["odds_place"][0])
#             if not odds_place_re:
#                 raise ContractFail("odds_place")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(requests)")


class OddsExactaContract(Contract):
    name = "odds_exacta_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsExactaItem
#         items = [o for o in output if isinstance(o, OddsExactaItem)]

#         if len(items) <= 1:
#             raise ContractFail("len(OddsExactaItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=5.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_1_re = re.match(r"^\d+$", item["horse_number_1"][0])
#             if not horse_number_1_re:
#                 raise ContractFail("horse_number_1")

#             horse_number_2_re = re.match(r"^\d+$", item["horse_number_2"][0])
#             if not horse_number_2_re:
#                 raise ContractFail("horse_number_2")

#             odds_re = re.match(r"^\d+\.\d+$", item["odds"][0])
#             if not odds_re:
#                 raise ContractFail("odds")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(Request)")


class OddsQuinellaContract(Contract):
    name = "odds_quinella_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsQuinellaItem
#         items = [o for o in output if isinstance(o, OddsQuinellaItem)]

#         if len(items) <= 1:
#             raise ContractFail("len(OddsQuinellaItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=6.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_1_re = re.match(r"^\d+$", item["horse_number_1"][0])
#             if not horse_number_1_re:
#                 raise ContractFail("horse_number_1")

#             horse_number_2_re = re.match(r"^\d+$", item["horse_number_2"][0])
#             if not horse_number_2_re:
#                 raise ContractFail("horse_number_2")

#             odds_re = re.match(r"^\d+\.\d+$", item["odds"][0])
#             if not odds_re:
#                 raise ContractFail("odds")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(Request)")


class OddsQuinellaPlaceContract(Contract):
    name = "odds_quinella_place_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsQuinellaPlaceItem
#         items = [o for o in output if isinstance(o, OddsQuinellaPlaceItem)]

#         if len(items) <= 1:
#             raise ContractFail("len(OddsQuinellaPlaceItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=7.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_1_re = re.match(r"^\d+$", item["horse_number_1"][0])
#             if not horse_number_1_re:
#                 raise ContractFail("horse_number_1")

#             horse_number_2_re = re.match(r"^\d+$", item["horse_number_2"][0])
#             if not horse_number_2_re:
#                 raise ContractFail("horse_number_2")

#             odds_lower_re = re.match(r"^\d+\.\d+$", item["odds_lower"][0])
#             if not odds_lower_re:
#                 raise ContractFail("odds_lower")

#             odds_upper_re = re.match(r"^\d+\.\d+$", item["odds_upper"][0])
#             if not odds_upper_re:
#                 raise ContractFail("odds_upper")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(Request)")


class OddsTrifectaContract(Contract):
    name = "odds_trifecta_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsTrifectaItem
#         items = [o for o in output if isinstance(o, OddsTrifectaItem)]

#         if len(items) <= 1:
#             raise ContractFail("len(OddsTrifectaItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=8.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_re = re.match(r"^\d+ → \d+ → \d+$", item["horse_number"][0])
#             if not horse_number_re:
#                 raise ContractFail("horse_number")

#             odds_re = re.match(r"^\d+\.\d+$", item["odds"][0])
#             if not odds_re:
#                 raise ContractFail("odds")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(Request)")


class OddsTrioContract(Contract):
    name = "odds_trio_contract"

    def post_process(self, output):
        pass
#         # Check item - OddsTrioItem
#         items = [o for o in output if isinstance(o, OddsTrioItem)]

#         if len(items) <= 1:
#             raise ContractFail("len(OddsTrioItem)")

#         for item in items:
#             odds_url_re = re.match(r"^https://www\.oddspark\.com/keiba/Odds\.do\?.*betType=9.*$", item["odds_url"][0])
#             if not odds_url_re:
#                 raise ContractFail("odds_url")

#             horse_number_1_2_re = re.match(r"^\d+-\d+$", item["horse_number_1_2"][0])
#             if not horse_number_1_2_re:
#                 raise ContractFail("horse_number_1_2")

#             horse_number_3_re = re.match(r"^\d+$", item["horse_number_3"][0])
#             if not horse_number_3_re:
#                 raise ContractFail("horse_number_3")

#             odds_re = re.match(r"^\d+\.\d+$", item["odds"][0])
#             if not odds_re:
#                 raise ContractFail("odds")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(Request)")


class RaceResultContract(Contract):
    name = "race_result_contract"

    def post_process(self, output):
        #
        # Check items
        #

        # レース結果
        items = [o for o in output if isinstance(o, RaceResultItem)]

        assert len(items) == 16

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["1"]
        assert i["bracket_number"] == ["6"]
        assert i["horse_number"] == ["12"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018101222/"]
        assert i["arrival_time"] == ["1:13.9"]
        assert i["arrival_margin"] == [""]
        assert i["final_600_meters_time"] == ["37.8"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["2"]
        assert i["bracket_number"] == ["7"]
        assert i["horse_number"] == ["14"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018102660/"]
        assert i["arrival_time"] == ["1:14.3"]
        assert i["arrival_margin"] == ["2"]
        assert i["final_600_meters_time"] == ["37.9"]

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["3"]
        assert i["bracket_number"] == ["6"]
        assert i["horse_number"] == ["11"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2019106574/"]
        assert i["arrival_time"] == ["1:14.3"]
        assert i["arrival_margin"] == ["アタマ"]
        assert i["final_600_meters_time"] == ["38.3"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["15"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["15"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103916/"]
        assert i["arrival_time"] == ["1:16.5"]
        assert i["arrival_margin"] == ["3"]
        assert i["final_600_meters_time"] == ["39.5"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["16"]
        assert i["bracket_number"] == ["5"]
        assert i["horse_number"] == ["10"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2019102218/"]
        assert i["arrival_time"] == ["1:17.6"]
        assert i["arrival_margin"] == ["5"]
        assert i["final_600_meters_time"] == ["41.6"]

        # 払戻しデータ
        items = [o for o in output if isinstance(o, RacePayoffItem)]

        assert len(items) == 9

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["単勝"]
        assert i["horse_number"] == ["12"]
        assert i["payoff_money"] == ["150円"]
        assert i["favorite_order"] == ["1人気"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["複勝"]
        assert i["horse_number"] == ["12 14 11"]
        assert i["payoff_money"] == ["100円170円150円"]
        assert i["favorite_order"] == ["1人気3人気2人気"]

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["枠連"]
        assert i["horse_number"] == ["6 7"]
        assert i["payoff_money"] == ["580円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[3]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["馬連"]
        assert i["horse_number"] == ["12 14"]
        assert i["payoff_money"] == ["740円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[4]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["ワイド"]
        assert i["horse_number"] == ["12 14 11 12 11 14"]
        assert i["payoff_money"] == ["320円240円790円"]
        assert i["favorite_order"] == ["2人気1人気9人気"]

        i = items[5]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["枠単"]
        assert i["horse_number"] == ["6 7"]
        assert i["payoff_money"] == ["670円"]
        assert i["favorite_order"] == ["3人気"]

        i = items[6]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["馬単"]
        assert i["horse_number"] == ["12 14"]
        assert i["payoff_money"] == ["890円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[7]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["3連複"]
        assert i["horse_number"] == ["11 12 14"]
        assert i["payoff_money"] == ["1,170円"]
        assert i["favorite_order"] == ["1人気"]

        i = items[8]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["3連単"]
        assert i["horse_number"] == ["12 14 11"]
        assert i["payoff_money"] == ["3,240円"]
        assert i["favorite_order"] == ["3人気"]

        # コーナー通過順位データ
        items = [o for o in output if isinstance(o, RaceCornerPassingOrderItem)]

        assert len(items) == 2

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_corner_passing_order"]
        assert i["race_id"] == ["202344111410"]
        assert i["corner_name"] == ["3コーナー"]
        assert i["passing_order"] == ["(10,11),12,13,14,1,16,15,9,6,3,2,8,5,7,4"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_corner_passing_order"]
        assert i["race_id"] == ["202344111410"]
        assert i["corner_name"] == ["4コーナー"]
        assert i["passing_order"] == ["11,12,10,(1,14,13),16,9,3,6,15,2,8,5,7,4"]

        # ラップタイムデータ
        items = [o for o in output if isinstance(o, RaceLaptimeItem)]

        assert len(items) == 3

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['200m', '400m', '600m', '800m', '1000m', '1200m']

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['12.7', '24.0', '36.0', '48.6', '1:00.7', '1:13.9']

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['12.7', '11.3', '12.0', '12.6', '12.1', '13.2']
