import logging

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request


logger = logging.getLogger(__name__)


class ScheduleListContract(Contract):
    name = "schedule_list"

    def post_process(self, output):
        logger.debug("ScheduleListContract#post_process: start")

        # Check requests
        requests = [o for o in output if isinstance(o, Request)]
        if len(requests) < 1:
            raise ContractFail("Empty requests")

        previous_calendar_page_requests = [r for r in requests if r.url.startswith("https://www.oddspark.com/keiba/KaisaiCalendar.do?")]
        if len(previous_calendar_page_requests) != 1:
            raise ContractFail("Previous calendar page not found")

        race_refund_list_page_requests = [r for r in requests if r.url.startswith("https://www.oddspark.com/keiba/RaceRefund.do?")]
        if len(race_refund_list_page_requests) == 0:
            raise ContractFail("Race refund list page not found")
