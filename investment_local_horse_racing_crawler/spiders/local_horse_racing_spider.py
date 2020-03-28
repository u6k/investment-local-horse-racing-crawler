import scrapy


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    start_urls = [
        "https://www.oddspark.com/keiba/KaisaiCalendar.do",
    ]

    def parse(self, response):
        """ Parse calendar page.

        @url https://www.oddspark.com/keiba/KaisaiCalendar.do
        @test
        """

        self.logger.info(f"#parse: start: url={response.url}")

        title = response.xpath("//title").get()
        self.logger.info(f"#parse: title={title}")
