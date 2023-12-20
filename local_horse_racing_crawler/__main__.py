import argparse
import os
from datetime import datetime
from urllib.parse import urlparse

from local_horse_racing_crawler.crawl_racelist import crawl_race, create_racelist
from local_horse_racing_crawler.middlewares import S3Client

#
# S3接続
#

aws_settings = {
    "AWS_ENDPOINT_URL": os.environ["AWS_ENDPOINT_URL"],
    "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
    "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
    "AWS_S3_CACHE_BUCKET": os.environ["AWS_S3_CACHE_BUCKET"],
    "AWS_S3_CACHE_FOLDER": os.environ["AWS_S3_CACHE_FOLDER"],
    "AWS_S3_FEED_URL": os.environ["AWS_S3_FEED_URL"],
    "AWS_S3_RACELIST_FOLDER": os.environ["AWS_S3_RACELIST_FOLDER"],
}

s3_client = S3Client(aws_settings)


#
# メイン処理
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task")

    args = parser.parse_args()

    if args.task == "create_racelist":
        s3_feed_url = urlparse(aws_settings["AWS_S3_FEED_URL"])
        s3_feed_path = s3_feed_url.path[1:]
        target_date = datetime.strptime(os.environ["TARGET_DATE"], "%Y-%m-%d")
        s3_racelist_folder = os.environ["AWS_S3_RACELIST_FOLDER"]

        create_racelist(s3_client, s3_feed_path, target_date, s3_racelist_folder)

    elif args.task == "crawl_race":
        s3_racelist_folder = aws_settings["AWS_S3_RACELIST_FOLDER"]
        target_date = datetime.strptime(os.environ["TARGET_DATE"], "%Y-%m-%d")
        queue_count = int(os.environ["CRAWL_QUEUE_COUNT"])

        crawl_race(s3_client, s3_racelist_folder, target_date, queue_count)

    else:
        parser.print_help()
