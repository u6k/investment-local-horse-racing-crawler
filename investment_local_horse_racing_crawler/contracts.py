import logging

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request


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
