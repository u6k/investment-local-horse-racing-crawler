import scrapy


class LocalHorseRacingSpider(scrapy.Spider):
    name = "local_horse_racing"

    start_urls = [
        "https://www.oddspark.com/keiba/KaisaiCalendar.do",
    ]

    def parse(self, response):
        self.logger.debug(f"#parse: start: url={response.url}")

        title = response.xpath("//title").get()
        self.logger.debug(f"#parse: title={title}")
