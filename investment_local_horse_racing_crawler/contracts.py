import logging

from scrapy.contracts import Contract


logger = logging.getLogger(__name__)


class TestContract(Contract):
    name = "test"

    def post_process(self, output):
        logger.debug("TestContract#post_process: start")
