import logging

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

from investment_local_horse_racing_crawler.scrapy.items import OddsWinPlaceItem, RaceResultItem, RacePayoffItem, HorseItem, JockeyItem, TrainerItem

logger = logging.getLogger(__name__)


class ScheduleListContract(Contract):
    name = "schedule_list"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]
        if len(requests) == 0:
            raise ContractFail("Empty requests")

        # Check url pattern
        count = sum(r.url.startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do?") for r in requests)
        if count != 1:
            raise ContractFail("Previous calendar page not found")

        count = sum(r.url.startswith("https://www.oddspark.com/keiba/RaceRefund.do?") for r in requests)
        if count == 0:
            raise ContractFail("Race refund list page not found")

        # Check unknown url
        for r in requests:
            if r.url.startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do?"):
                continue

            if r.url.startswith("https://www.oddspark.com/keiba/RaceRefund.do?"):
                continue

            raise ContractFail(f"Unknown url: {r.url}")


class RaceRefundListContract(Contract):
    name = "race_refund_list"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]
        if len(requests) == 0:
            raise ContractFail("Empty requests")

        # Check unknown url
        for r in requests:
            if r.url.startswith("https://www.oddspark.com/keiba/RaceList.do?"):
                continue

            raise ContractFail(f"Unknown url: {r.url}")


class RaceDenmaContract(Contract):
    name = "race_denma"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        # Check url pattern
        count = sum(r.url.startswith("https://www.oddspark.com/keiba/Odds.do?") for r in requests)
        if count != 1:
            raise ContractFail("Odds page not found")

        count = sum(r.url.startswith("https://www.oddspark.com/keiba/RaceResult.do?") for r in requests)
        if count != 1:
            raise ContractFail("Race result page not found")

        count = sum(r.url.startswith("https://www.oddspark.com/keiba/HorseDetail.do?") for r in requests)
        if count == 0:
            raise ContractFail("Horse page not found")

        count = sum(r.url.startswith("https://www.oddspark.com/keiba/JockeyDetail.do?") for r in requests)
        if count == 0:
            raise ContractFail("Jockey page not found")

        count = sum(r.url.startswith("https://www.oddspark.com/keiba/TrainerDetail.do?") for r in requests)
        if count == 0:
            raise ContractFail("Trainer page not found")

        # Check unknown url
        for r in requests:
            if r.url.startswith("https://www.oddspark.com/keiba/Odds.do?"):
                continue

            if r.url.startswith("https://www.oddspark.com/keiba/RaceResult.do?"):
                continue

            if r.url.startswith("https://www.oddspark.com/keiba/HorseDetail.do?"):
                continue

            if r.url.startswith("https://www.oddspark.com/keiba/JockeyDetail.do?"):
                continue

            if r.url.startswith("https://www.oddspark.com/keiba/TrainerDetail.do?"):
                continue

            raise ContractFail(f"Unknown url: {r.url}")


class OddsWinContract(Contract):
    name = "odds_win"

    def post_process(self, output):
        count = sum(isinstance(o, OddsWinPlaceItem) for o in output)
        if count == 0:
            raise ContractFail("Empty output")

        for o in output:
            if isinstance(o, OddsWinPlaceItem):
                continue

            raise ContractFail("Unknown output")


class RaceResultContract(Contract):
    name = "race_result"

    def post_process(self, output):
        count = sum(isinstance(o, RaceResultItem) for o in output)
        if count == 0:
            raise ContractFail("Empty race result")

        count = sum(isinstance(o, RacePayoffItem) for o in output)
        if count == 0:
            raise ContractFail("Empty race payoff")

        for o in output:
            if isinstance(o, RaceResultItem):
                continue

            if isinstance(o, RacePayoffItem):
                continue

            raise ContractFail("Unknown output")


class HorseContract(Contract):
    name = "horse"

    def post_process(self, output):
        count = sum(isinstance(o, HorseItem) for o in output)
        if count == 0:
            raise ContractFail("Empty horse")

        for o in output:
            if isinstance(o, HorseItem):
                continue

            raise ContractFail("Unknown output")


class JockeyContract(Contract):
    name = "jockey"

    def post_process(self, output):
        count = sum(isinstance(o, JockeyItem) for o in output)
        if count == 0:
            raise ContractFail("Empty jockey")

        for o in output:
            if isinstance(o, JockeyItem):
                continue

            raise ContractFail("Unknown output")


class TrainerContract(Contract):
    name = "trainer"

    def post_process(self, output):
        count = sum(isinstance(o, TrainerItem) for o in output)
        if count == 0:
            raise ContractFail("Empty trainer")

        for o in output:
            if isinstance(o, TrainerItem):
                continue

            raise ContractFail("Unknown output")