import scrapy


class KakuninSpider(scrapy.Spider):
    name = "kakunin"

    def __init__(self, *args, **kwargs):
        super(KakuninSpider, self).__init__(*args, **kwargs)

        self.start_urls = ["https://kakunin.net/kun/"]

    def parse(self, response):
        pass
