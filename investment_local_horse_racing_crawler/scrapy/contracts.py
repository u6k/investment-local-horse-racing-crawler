import re
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

from investment_local_horse_racing_crawler.scrapy.items import CalendarItem, RaceSummaryMiniItem
from investment_local_horse_racing_crawler.app_logging import get_logger


logger = get_logger(__name__)



class CalendarContract(Contract):
    name = "calendar"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, CalendarItem)]

        if len(items) != 1:
            raise ContractFail("CalendarItems is not 1")

        item = items[0]

        if len(item["calendar_url"]) != 1:
            raise ContractFail("len(item.calendar_url) is not 1")

        if not item["calendar_url"][0].startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do"):
            raise ContractFail("item.calendar_url is invalid")

        if len(item["race_list_urls"]) <= 1:
            raise ContractFail(f"len(item.race_list_urls) <= 1")
        
        for race_list_url in item["race_list_urls"]:
            if not race_list_url.startswith("/keiba/OneDayRaceList.do?"):
                raise ContractFail(f"race_list_url is invalid")

        # Check requests
        requests = [o for o in output if isinstance(o, Request)]
        
        if len(requests) <= 1:
            raise ContractFail(f"len(requests) <= 1")

        for request in requests:
            if not request.url.startswith("https://www.oddspark.com/keiba/OneDayRaceList.do?"):
                raise ContractFail(f"request is invalid")




class OneDayRaceListContract(Contract):
    name = "one_day_race_list"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, RaceSummaryMiniItem)]

        if len(items) != 11:
            raise ContractFail("len(RaceSummaryMiniItem) != 11")

        for item in items:
            if len(item["race_list_url"]) != 1:
                raise ContractFail("len(race_list_url) != 1")
            if not item["race_list_url"][0].startswith("https://www.oddspark.com/keiba/OneDayRaceList.do?"):
                raise ContractFail("race_list_url[0] is invalid")

            if len(item["race_name"]) != 1:
                raise ContractFail("len(race_name) != 1")
            if not item["race_name"][0]:
                raise ContractFail("race_name[0] is empty")

            if len(item["race_denma_url"]) != 1:
                raise ContractFail("len(race_denma_url) != 1")
            if not item["race_denma_url"][0].startswith("/keiba/RaceList.do?"):
                raise ContractFail("race_denma_url[0] is invalid")

            if len(item["course_length"]) != 1:
                raise ContractFail("len(course_length) != 1")
            if not item["course_length"][0]:
                raise ContractFail("course_length[0] is empty")

            if len(item["start_time"]) != 1:
                raise ContractFail("len(start_time) != 1")
            start_time_re = re.match("^\d+:\d+", item["start_time"][0])
            if not start_time_re:
                raise ContractFail("start_time is invalid pattern")

        # Check requests
        requests = [o for o in output if isinstance(o, Request)]
        
        if len(requests) != 11:
            raise ContractFail(f"len(requests) != 11")

        for request in requests:
            if not request.url.startswith("https://www.oddspark.com/keiba/RaceList.do?"):
                raise ContractFail("request is invalid")




class ScheduleListContract(Contract):
    name = "schedule_list"

    def post_process(self, output):
        pass
        # # Check requests
        # requests = [o for o in output if isinstance(o, Request)]
        # if len(requests) == 0:
        #     raise ContractFail("Empty requests")

        # # Check url pattern
        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do?") for r in requests)
        # if count != 1:
        #     raise ContractFail("Previous calendar page not found")

        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/RaceRefund.do?") for r in requests)
        # if count == 0:
        #     raise ContractFail("Race refund list page not found")

        # # Check unknown url
        # for r in requests:
        #     if r.url.startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/RaceRefund.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/OneDayRaceList.do?"):
        #         continue

        #     raise ContractFail(f"Unknown url: {r.url}")


class RaceRefundListContract(Contract):
    name = "race_refund_list"

    def post_process(self, output):
        pass
        # # Check requests
        # requests = [o for o in output if isinstance(o, Request)]
        # if len(requests) == 0:
        #     raise ContractFail("Empty requests")

        # # Check unknown url
        # for r in requests:
        #     if r.url.startswith("https://www.oddspark.com/keiba/OneDayRaceList.do?"):
        #         continue

        #     raise ContractFail(f"Unknown url: {r.url}")


class RaceDenmaContract(Contract):
    name = "race_denma"

    def post_process(self, output):
        pass
        # # Check requests
        # requests = [o for o in output if isinstance(o, Request)]

        # # Check url pattern
        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/Odds.do?") for r in requests)
        # if count != 1:
        #     raise ContractFail("Odds page not found")

        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/RaceResult.do?") for r in requests)
        # if count != 1:
        #     raise ContractFail("Race result page not found")

        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/HorseDetail.do?") for r in requests)
        # if count == 0:
        #     raise ContractFail("Horse page not found")

        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/JockeyDetail.do?") for r in requests)
        # if count == 0:
        #     raise ContractFail("Jockey page not found")

        # count = sum(r.url.startswith("https://www.oddspark.com/keiba/TrainerDetail.do?") for r in requests)
        # if count == 0:
        #     raise ContractFail("Trainer page not found")

        # # Check unknown url
        # for r in requests:
        #     if r.url.startswith("https://www.oddspark.com/keiba/Odds.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/RaceResult.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/HorseDetail.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/JockeyDetail.do?"):
        #         continue

        #     if r.url.startswith("https://www.oddspark.com/keiba/TrainerDetail.do?"):
        #         continue

        #     raise ContractFail(f"Unknown url: {r.url}")


class OddsWinContract(Contract):
    name = "odds_win"

    def post_process(self, output):
        pass
        # count = sum(isinstance(o, OddsWinPlaceItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty output")

        # for o in output:
        #     if isinstance(o, OddsWinPlaceItem):
        #         continue

        #     raise ContractFail("Unknown output")


class RaceResultContract(Contract):
    name = "race_result"

    def post_process(self, output):
        pass
        # count = sum(isinstance(o, RaceResultItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty race result")

        # count = sum(isinstance(o, RacePayoffItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty race payoff")

        # for o in output:
        #     if isinstance(o, RaceResultItem):
        #         continue

        #     if isinstance(o, RacePayoffItem):
        #         continue

        #     raise ContractFail("Unknown output")


class HorseContract(Contract):
    name = "horse"

    def post_process(self, output):
        pass
        # count = sum(isinstance(o, HorseItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty horse")

        # for o in output:
        #     if isinstance(o, HorseItem):
        #         continue

        #     raise ContractFail("Unknown output")


class JockeyContract(Contract):
    name = "jockey"

    def post_process(self, output):
        pass
        # count = sum(isinstance(o, JockeyItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty jockey")

        # for o in output:
        #     if isinstance(o, JockeyItem):
        #         continue

        #     raise ContractFail("Unknown output")


class TrainerContract(Contract):
    name = "trainer"

    def post_process(self, output):
        pass
        # count = sum(isinstance(o, TrainerItem) for o in output)
        # if count == 0:
        #     raise ContractFail("Empty trainer")

        # for o in output:
        #     if isinstance(o, TrainerItem):
        #         continue

        #     raise ContractFail("Unknown output")
