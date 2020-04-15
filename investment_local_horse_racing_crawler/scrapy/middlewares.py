# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import os
import boto3
import pickle
from scrapy import signals
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class InvestmentLocalHorseRacingCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class InvestmentLocalHorseRacingCrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class S3CacheStorage(object):

    def __init__(self, settings):
        logger.debug("#init: start")

        self.s3_endpoint = settings["S3_ENDPOINT"]
        self.s3_region = settings["S3_REGION"]
        self.s3_access_key = settings["S3_ACCESS_KEY"]
        self.s3_secret_key = settings["S3_SECRET_KEY"]
        self.s3_bucket = settings["S3_BUCKET"]
        self.s3_folder = settings["S3_FOLDER"]

        logger.debug(f"#init: s3_endpoint={self.s3_endpoint}, s3_region={self.s3_region}, s3_bucket={self.s3_bucket}, s3_folder={self.s3_folder}")

    def open_spider(self, spider):
        logger.debug("#open_spider: start: spider=%s" % spider)

        self.s3_client = boto3.resource(
            "s3",
            endpoint_url=self.s3_endpoint,
            aws_access_key_id=self.s3_access_key,
            aws_secret_access_key=self.s3_secret_key,
            region_name=self.s3_region)

        self.s3_bucket_obj = self.s3_client.Bucket(self.s3_bucket)
        if self.s3_bucket_obj.creation_date:
            logger.debug("#open_spider: bucket exist")
        else:
            self.s3_bucket_obj.create()
            logger.debug("#open_spider: bucket created")

    def close_spider(self, spider):
        logger.debug("#close_spider")

    def retrieve_response(self, spider, request):
        logger.debug("#retrieve_response: start: url=%s" % request.url)

        rpath = self._get_request_path(spider, request)
        logger.debug("#retrieve_response: cache path=%s" % rpath)

        s3_obj = self.s3_bucket_obj.Object(rpath)

        try:
            s3_obj.last_modified
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                logger.debug("#retrieve_response: cache_nothing")
                return
            else:
                raise err

        if spider.recache_race and (("KaisaiCalendar.do" in request.url) or ("RaceRefund.do" in request.url) or ("RaceList.do" in request.url) or ("Odds.do" in request.url) or ("RaceResult.do" in request.url)):
            logger.debug("#retrieve_response: re-cache race")
            return

        if spider.recache_horse and (("HorseDetail.do" in request.url) or ("JockeyDetail.do" in request.url) or ("TrainerDetail.do" in request.url)):
            logger.debug("#retrieve_response: re-cache horse/jockey/trainer")
            return

        data = pickle.loads(s3_obj.get()["Body"].read())

        url = data["url"]
        status = data["status"]
        headers = Headers(data["headers"])
        body = data["body"]
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)

        logger.debug("#retrieve_response: cache_exist")

        return response

    def store_response(self, spider, request, response):
        logger.debug("#store_response: start: url=%s" % response.url)

        rpath = self._get_request_path(spider, request)
        logger.debug("#store_response: cache path=%s" % rpath)

        data = {
            "status": response.status,
            "url": response.url,
            "headers": dict(response.headers),
            "body": response.body,
        }

        data_obj = pickle.dumps(data)

        self.s3_bucket_obj.Object(rpath).put(Body=data_obj)

        logger.debug("#store_response: data put")

    def _get_request_path(self, spider, request):
        key = request_fingerprint(request)
        return os.path.join(self.s3_folder, key[0:2], key)
