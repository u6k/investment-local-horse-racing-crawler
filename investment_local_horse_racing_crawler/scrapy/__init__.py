from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from billiard import Process


class CrawlerScript():
    def __init__(self):
        settings = get_project_settings()
        self.crawler = CrawlerProcess(settings, install_root_handler=False)

    def _crawl(self, start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse):
        self.crawler.crawl("local_horse_racing", start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse)
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, start_url, recrawl_period, recrawl_race_id, recache_race, recache_horse):
        process = Process(target=self._crawl, kwargs={"start_url": start_url, "recrawl_period": recrawl_period, "recrawl_race_id": recrawl_race_id, "recache_race": recache_race, "recache_horse": recache_horse})
        process.start()
        process.join()


crawler = CrawlerScript()
