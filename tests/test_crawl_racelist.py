import os
from datetime import datetime
from urllib.parse import urlparse

from local_horse_racing_crawler import crawl_racelist, middlewares

aws_settings = {
    "AWS_ENDPOINT_URL": os.environ["AWS_ENDPOINT_URL"],
    "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
    "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
    "AWS_S3_CACHE_BUCKET": os.environ["AWS_S3_CACHE_BUCKET"],
    "AWS_S3_CACHE_FOLDER": os.environ["AWS_S3_CACHE_FOLDER"],
    "AWS_S3_FEED_URL": os.environ["AWS_S3_FEED_URL"],
    "AWS_S3_RACELIST_FOLDER": os.environ["AWS_S3_RACELIST_FOLDER"],
}

s3_client = middlewares.S3Client(aws_settings)

s3_feed_url = urlparse(aws_settings["AWS_S3_FEED_URL"])
s3_feed_path = s3_feed_url.path[1:]
target_date = datetime(2023, 12, 15)


def test_get_feed():
    json_data = crawl_racelist.get_feed(s3_client, s3_feed_path)

    assert len(json_data) > 0


def test_parse_race_info():
    json_item = {
        "url": ["https://nar.netkeiba.com/race/shutuba.html?race_id=202345121504#race_info"],
        "race_id": ["202345121504"],
        "race_round": ["4R"],
        "race_name": ["ジングルベル賞(2歳)"],
        "race_data1": ["16:30発走 / ダ1500m (左) / 天候:曇 / 馬場:稍"],
        "race_data2": ["10回 川崎 5日目 サラ系２歳 2歳       11頭 本賞金:250.0、100.0、62.5、37.5、25.0万円"],
        "race_data3": ["ジングルベル賞 出馬表 | 2023年12月15日 川崎4R 地方競馬レース情報 - netkeiba.com"]
    }

    dict_race_info = crawl_racelist.parse_race_info(json_item)

    assert dict_race_info["race_id"] == "202345121504"
    assert dict_race_info["race_round"] == 4
    assert dict_race_info["race_name"] == "ジングルベル賞(2歳)"
    assert dict_race_info["start_datetime"] == datetime(2023, 12, 15, 16, 30, 0)


def test_parse_feed():
    json_data = crawl_racelist.get_feed(s3_client, s3_feed_path)

    df_race_info = crawl_racelist.parse_feed(json_data)

    assert len(df_race_info) > 0


def test_extract_racelist():
    json_data = crawl_racelist.get_feed(s3_client, s3_feed_path)
    df_race_info = crawl_racelist.parse_feed(json_data)

    df_tmp = crawl_racelist.extract_racelist(df_race_info, datetime(2023, 12, 15))
    assert len(df_tmp) > 0

    df_tmp = crawl_racelist.extract_racelist(df_race_info, datetime(2023, 1, 1))
    assert len(df_tmp) == 0


def test_create_racelist():
    crawl_racelist.create_racelist(s3_client, s3_feed_path, target_date, aws_settings["AWS_S3_RACELIST_FOLDER"])


def test_find_target_racelist():
    df_racelist = crawl_racelist.get_racelist(s3_client, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)
    df_racelist.loc[df_racelist["crawl_start_datetime"] < "2023-12-15 12:00:00", "crawl_finish_datetime"] = datetime(2023, 12, 15, 12, 10, 0)

    now_datetime = datetime(2023, 12, 15, 14, 0, 0)
    df_target_racelist = crawl_racelist.find_target_racelist(df_racelist, now_datetime)

    assert len(df_target_racelist) == 19


def test_crawl_race_in_subprocess():
    df_racelist = crawl_racelist.get_racelist(s3_client, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)
    df_racelist.loc[df_racelist["crawl_start_datetime"] < "2023-12-15 12:00:00", "crawl_finish_datetime"] = datetime(2023, 12, 15, 12, 10, 0)

    now_datetime = datetime(2023, 12, 15, 14, 0, 0)
    df_target_racelist = crawl_racelist.find_target_racelist(df_racelist, now_datetime)

    crawl_queue = {}
    queue_count = 3

    crawl_queue = crawl_racelist.crawl_race_in_subprocess(df_target_racelist, crawl_queue, queue_count)

    assert len(crawl_queue) == 3


def test_find_crawl_finished_race_items():
    df_racelist = crawl_racelist.get_racelist(s3_client, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)
    df_racelist.loc[df_racelist["crawl_start_datetime"] < "2023-12-15 12:00:00", "crawl_finish_datetime"] = datetime(2023, 12, 15, 12, 10, 0)

    now_datetime = datetime(2023, 12, 15, 14, 0, 0)
    df_target_racelist = crawl_racelist.find_target_racelist(df_racelist, now_datetime)

    crawl_queue = {}
    queue_count = 3

    crawl_queue = crawl_racelist.crawl_race_in_subprocess(df_target_racelist, crawl_queue, queue_count)

    finished_race_items = crawl_racelist.find_crawl_finished_race_items(crawl_queue)

    assert len(finished_race_items) == 3


def test_update_racelist():
    df_racelist = crawl_racelist.get_racelist(s3_client, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)
    df_racelist.loc[df_racelist["crawl_start_datetime"] < "2023-12-15 12:00:00", "crawl_finish_datetime"] = datetime(2023, 12, 15, 12, 10, 0)

    now_datetime = datetime(2023, 12, 15, 14, 0, 0)
    df_target_racelist = crawl_racelist.find_target_racelist(df_racelist, now_datetime)

    crawl_queue = {}
    queue_count = 3

    crawl_queue = crawl_racelist.crawl_race_in_subprocess(df_target_racelist, crawl_queue, queue_count)

    finished_race_items = crawl_racelist.find_crawl_finished_race_items(crawl_queue)

    df_racelist, crawl_queue = crawl_racelist.update_racelist(s3_client, finished_race_items, datetime.now(), df_racelist, crawl_queue, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)

    assert len(crawl_racelist.find_target_racelist(df_racelist, datetime.now())) == 102
    assert len(crawl_queue) == 0


def test_find_crawl_unfinished_racelist():
    df_racelist = crawl_racelist.get_racelist(s3_client, aws_settings["AWS_S3_RACELIST_FOLDER"], target_date)
    df_racelist["crawl_finish_datetime"] = None
    df_racelist.loc[df_racelist["crawl_start_datetime"] < "2023-12-15 12:00:00", "crawl_finish_datetime"] = datetime(2023, 12, 15, 12, 10, 0)

    df_unfinished_racelist = crawl_racelist.find_crawl_unfinished_racelist(df_racelist)

    assert len(df_unfinished_racelist) == 105
