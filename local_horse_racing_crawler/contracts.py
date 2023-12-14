from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

# from local_horse_racing_crawler.items import CalendarItem, HorseItem, JockeyItem, OddsExactaItem, OddsQuinellaItem, OddsQuinellaPlaceItem, OddsTrifectaItem, OddsTrioItem, OddsWinPlaceItem, RaceCornerPassingOrderItem, RaceDenmaItem, RaceInfoItem, RaceInfoMiniItem, RaceRefundItem, RaceResultItem, TrainerItem


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
        pass


# TODO
# class OneDayRaceListContract(Contract):
#     name = "one_day_race_list_contract"

#     def post_process(self, output):
#         # Check item
#         items = [o for o in output if isinstance(o, RaceInfoMiniItem)]

#         if len(items) != 11:
#             raise ContractFail("len(RaceInfoMiniItem) != 11")

#         for item in items:
#             if len(item["race_list_url"]) != 1:
#                 raise ContractFail("len(race_list_url) != 1")
#             if not item["race_list_url"][0].startswith("https://www.oddspark.com/keiba/OneDayRaceList.do?"):
#                 raise ContractFail("race_list_url[0] is invalid")

#             if len(item["race_name"]) != 1:
#                 raise ContractFail("len(race_name) != 1")
#             if not item["race_name"][0]:
#                 raise ContractFail("race_name[0] is empty")

#             if len(item["race_denma_url"]) != 1:
#                 raise ContractFail("len(race_denma_url) != 1")
#             if not item["race_denma_url"][0].startswith("/keiba/RaceList.do?"):
#                 raise ContractFail("race_denma_url[0] is invalid")

#             if len(item["course_length"]) != 1:
#                 raise ContractFail("len(course_length) != 1")
#             if not item["course_length"][0]:
#                 raise ContractFail("course_length[0] is empty")

#             if len(item["start_time"]) != 1:
#                 raise ContractFail("len(start_time) != 1")
#             start_time_re = re.match(r"^\d+:\d+$", item["start_time"][0])
#             if not start_time_re:
#                 raise ContractFail("start_time is invalid pattern")

#         # Check requests
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 11:
#             raise ContractFail("len(requests) != 11")

#         for request in requests:
#             if not request.url.startswith("https://www.oddspark.com/keiba/RaceList.do?"):
#                 raise ContractFail("request is invalid")


# class RaceDenmaContract(Contract):
#     name = "race_denma_contract"

#     def post_process(self, output):
#         # Check item - RaceInfoItem
#         items = [o for o in output if isinstance(o, RaceInfoItem)]

#         if len(items) != 1:
#             raise ContractFail("len(RaceInfoItem) != 1")

#         item = items[0]

#         if not item["race_denma_url"][0].startswith("https://www.oddspark.com/keiba/RaceList.do?"):
#             raise ContractFail("race_denma_url is invalid")

#         race_round_re = re.match(r"^R\d+$", item["race_round"][0])
#         if not race_round_re:
#             raise ContractFail("race_round is invalid")

#         if not item["race_name"][0]:
#             raise ContractFail("race_name is empty")

#         start_date_re = re.match(r"^\d{4}年\d{1,2}月\d{1,2}日\(\w\)$", item["start_date"][0])
#         if not start_date_re:
#             raise ContractFail("start_date is invalid")

#         if not item["place_name"][0]:
#             raise ContractFail("place_name is invalid")

#         course_type_length = re.match(r"^\w\d+m$", item["course_type_length"][0])
#         if not course_type_length:
#             raise ContractFail("course_type_length is invalid")

#         start_time_re = re.match(r"^発走時間 \d{1,2}:\d{1,2}$", item["start_time"][0])
#         if not start_time_re:
#             raise ContractFail("start_time is invalid")

#         if not item["weather_url"][0].startswith("/local/images/ico-tenki-"):
#             raise ContractFail("weather_url is invalid")

#         if "course_condition" in item:
#             if not item["course_condition"][0].startswith("/local/images/ico-baba-"):
#                 raise ContractFail("course_condition is invalid")

#         if "moisture" in item:
#             moisture_re = re.match(r"^[\d\.]+\%$", item["moisture"][0])
#             if not moisture_re:
#                 raise ContractFail("moisture is invalid")

#         prize_money_re = re.match(r"^.*賞金.*1着.*[\d,]+円.*2着.*[\d,]+円.*3着.*[\d,]+円.*4着.*[\d,]+円.*5着.*[\d,]+円.*$", item["prize_money"][0])
#         if not prize_money_re:
#             raise ContractFail("prize_money is invalid")

#         # Check item - RaceDenmaItem
#         items = [o for o in output if isinstance(o, RaceDenmaItem)]

#         if len(items) == 0:
#             raise ContractFail("len(RaceDenmaItem) == 0")

#         for item in items:
#             if not item["race_denma_url"][0].startswith("https://www.oddspark.com/keiba/RaceList.do?"):
#                 raise ContractFail("race_denma_url is invalid")

#             if not item["bracket_number"][0]:
#                 raise ContractFail("bracket_number is empty")

#             if not item["horse_number"][0]:
#                 raise ContractFail("horse_number is empty")

#             horse_url_re = re.match(r"^/keiba/HorseDetail\.do\?lineageNb=\d+$", item["horse_url"][0])
#             if not horse_url_re:
#                 raise ContractFail("horse_url is invalid")

#             jockey_url_re = re.match(r"^/keiba/JockeyDetail\.do\?jkyNb=\d+$", item["jockey_url"][0])
#             if not jockey_url_re:
#                 raise ContractFail("jockey_url is invalid")

#             jockey_weight_re = re.match(r"^.?\d+(\.\d+)?$", item["jockey_weight"][0])
#             if not jockey_weight_re:
#                 raise ContractFail("jockey_weight is invalid")

#             trainer_url_re = re.match(r"^/keiba/TrainerDetail\.do\?trainerNb=\d+$", item["trainer_url"][0])
#             if not trainer_url_re:
#                 raise ContractFail("trainer_url is invalid")

#             odds_win_favorite_re = re.match(r"^[\d\.]+ +\(\d+人気\)$", item["odds_win_favorite"][0])
#             if not odds_win_favorite_re:
#                 raise ContractFail("odds_win_favorite is invalid")

#             horse_weight_re = re.match(r"^\d+$", item["horse_weight"][0])
#             if not horse_weight_re:
#                 raise ContractFail("horse_weight is invalid")

#             horse_weight_diff_re = re.match(r"^[\+\-±]\d+$", item["horse_weight_diff"][0])
#             if not horse_weight_diff_re:
#                 raise ContractFail("horse_weight_diff is invalid")

#         # Check requests
#         requests = [o for o in output if isinstance(o, Request)]

#         count = sum(r.url.startswith("https://www.oddspark.com/keiba/Odds.do?") for r in requests)
#         if count <= 1:
#             raise ContractFail("Odds page not found")

#         count = sum(r.url.startswith("https://www.oddspark.com/keiba/RaceResult.do?") for r in requests)
#         if count != 1:
#             raise ContractFail("Race result page not found")

#         count = sum(r.url.startswith("https://www.oddspark.com/keiba/HorseDetail.do?lineageNb=") for r in requests)
#         if count <= 1:
#             raise ContractFail("Horse page not found")

#         count = sum(r.url.startswith("https://www.oddspark.com/keiba/JockeyDetail.do?jkyNb=") for r in requests)
#         if count <= 1:
#             raise ContractFail("Jockey page not found")

#         count = sum(r.url.startswith("https://www.oddspark.com/keiba/TrainerDetail.do?trainerNb=") for r in requests)
#         if count <= 1:
#             raise ContractFail("Trainer page not found")


# class RaceResultContract(Contract):
#     name = "race_result_contract"

#     def post_process(self, output):
#         # Check item - RaceResultItem
#         items = [o for o in output if isinstance(o, RaceResultItem)]

#         if len(items) == 0:
#             raise ContractFail("RaceResultItem is empty")

#         for item in items:
#             if not item["race_result_url"][0].startswith("https://www.oddspark.com/keiba/RaceResult.do?"):
#                 raise ContractFail("race_result_url is invalid")

#             if not item["result"][0]:
#                 raise ContractFail("result is invalid")

#             if not item["bracket_number"][0]:
#                 raise ContractFail("bracket_number is invalid")

#             if not item["horse_number"][0]:
#                 raise ContractFail("horse_number is invalid")

#             horse_url_re = re.match(r"^/keiba/HorseDetail\.do\?lineageNb=\d+$", item["horse_url"][0])
#             if not horse_url_re:
#                 raise ContractFail("horse_url is invalid")

#             arrival_time_re = re.match(r"^(\d+:)\d+\.\d+$", item["arrival_time"][0])
#             if not arrival_time_re:
#                 raise ContractFail("arrival_time is invalid")

#             if "arrival_margin" in item:
#                 if not item["arrival_margin"][0]:
#                     raise ContractFail("arrival_margin is invalid")

#             final_600_meters_time_re = re.match(r"^[\d\.]+$", item["final_600_meters_time"][0])
#             if not final_600_meters_time_re:
#                 raise ContractFail("final_600_meters_time is invalid")

#             corner_passing_order_re = re.match(r"^\d+\-\d+\-\d+\-\d+$", item["corner_passing_order"][0])
#             if not corner_passing_order_re:
#                 raise ContractFail("corner_passing_order is invalid")

#         # Check item - RaceCornerPassingOrderItem
#         items = [o for o in output if isinstance(o, RaceCornerPassingOrderItem)]

#         if len(items) != 4:
#             raise ContractFail("len(RaceCornerPassingOrderItem) != 4")

#         for item in items:
#             if not item["race_result_url"][0].startswith("https://www.oddspark.com/keiba/RaceResult.do?"):
#                 raise ContractFail("race_result_url is invalid")

#             corner_number_re = re.match(r"^.コーナー$", item["corner_number"][0])
#             if not corner_number_re:
#                 raise ContractFail("corner_number is invalid")

#             if not item["passing_order"][0]:
#                 raise ContractFail("passing_order is invalid")

#         # Check item - RaceRefundItem
#         items = [o for o in output if isinstance(o, RaceRefundItem)]

#         if len(items) == 0:
#             raise ContractFail("RaceRefundItem is empty")

#         for item in items:
#             if not item["race_result_url"][0].startswith("https://www.oddspark.com/keiba/RaceResult.do?"):
#                 raise ContractFail("race_result_url is invalid")

#             if not item["betting_type"][0]:
#                 raise ContractFail("betting_type is invalid")

#             if not item["horse_number"][0]:
#                 raise ContractFail("horse_number is invalid")

#             refund_money_re = re.match(r"^[\d\,]+円$", item["refund_money"][0])
#             if not refund_money_re:
#                 raise ContractFail("refund_money is invalid")

#             favorite_re = re.match(r"^\d+番人気$", item["favorite"][0])
#             if not favorite_re:
#                 raise ContractFail("favorite is invalid")

#         # Check requests
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("requests is not empty")


# class HorseContract(Contract):
#     name = "horse_contract"

#     def post_process(self, output):
#         # Check item
#         items = [o for o in output if isinstance(o, HorseItem)]

#         if len(items) != 1:
#             raise ContractFail("len(HorseItem)")

#         item = items[0]

#         horse_url_re = re.match(r"^https://www\.oddspark\.com/keiba/HorseDetail\.do\?lineageNb=\d+$", item["horse_url"][0])
#         if not horse_url_re:
#             raise ContractFail("horse_url")

#         if not item["horse_name"][0]:
#             raise ContractFail("horse_name")

#         gender_age_re = re.match(r"^\w+｜\d+ 歳$", item["gender_age"][0])
#         if not gender_age_re:
#             raise ContractFail("gender_age")

#         birthday_re = re.match(r"^\d{4}年\d{1,2}月\d{1,2}日$", item["birthday"][0])
#         if not birthday_re:
#             raise ContractFail("birthday")

#         coat_color_re = re.match(r"^\w+毛$", item["coat_color"][0])
#         if not coat_color_re:
#             raise ContractFail("coat_color")

#         trainer_url_re = re.match(r"^/keiba/TrainerDetail\.do\?trainerNb=\d+$", item["trainer_url"][0])
#         if not trainer_url_re:
#             raise ContractFail("trainer_url")

#         if not item["owner"][0]:
#             raise ContractFail("owner")

#         if not item["breeder"][0]:
#             raise ContractFail("breeder")

#         if not item["breeding_farm"][0]:
#             raise ContractFail("breeding_farm")

#         if not item["parent_horse_name_1"][0]:
#             raise ContractFail("parent_horse_name_1")

#         if not item["parent_horse_name_2"][0]:
#             raise ContractFail("parent_horse_name_2")

#         if not item["grand_parent_horse_name_1"][0]:
#             raise ContractFail("grand_parent_horse_name_1")

#         if not item["grand_parent_horse_name_2"][0]:
#             raise ContractFail("grand_parent_horse_name_2")

#         if not item["grand_parent_horse_name_3"][0]:
#             raise ContractFail("grand_parent_horse_name_3")

#         if not item["grand_parent_horse_name_4"][0]:
#             raise ContractFail("grand_parent_horse_name_4")

#         # Check request
#         requests = [o for o in output if isinstance(o, Request)]

#         if len(requests) != 0:
#             raise ContractFail("len(requests)")


# class JockeyContract(Contract):
#     name = "jockey_contract"

#     def post_process(self, output):
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


# class TrainerContract(Contract):
#     name = "trainer_contract"

#     def post_process(self, output):
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


# class OddsWinPlaceContract(Contract):
#     name = "odds_win_place_contract"

#     def post_process(self, output):
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


# class OddsQuinellaContract(Contract):
#     name = "odds_quinella_contract"

#     def post_process(self, output):
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


# class OddsExactaContract(Contract):
#     name = "odds_exacta_contract"

#     def post_process(self, output):
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


# class OddsQuinellaPlaceContract(Contract):
#     name = "odds_quinella_place_contract"

#     def post_process(self, output):
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


# class OddsTrioContract(Contract):
#     name = "odds_trio_contract"

#     def post_process(self, output):
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


# class OddsTrifectaContract(Contract):
#     name = "odds_trifecta_contract"

#     def post_process(self, output):
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
