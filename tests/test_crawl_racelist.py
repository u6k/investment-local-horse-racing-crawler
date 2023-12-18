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
}

s3_client = middlewares.S3Client(aws_settings)


def test_get_feed():
    s3_feed_url = urlparse(aws_settings["AWS_S3_FEED_URL"])
    s3_feed_path = s3_feed_url.path[1:]

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
    assert dict_race_info["course_type_id"] == 2
    assert dict_race_info["course_length"] == 1500
    assert dict_race_info["course_curve"] == "左"
    assert dict_race_info["weather_id"] == 2
    assert dict_race_info["course_condition"] == 2
    assert dict_race_info["prize_money_1"] == 250.0
    assert dict_race_info["prize_money_2"] == 100.0
    assert dict_race_info["prize_money_3"] == 62.5
    assert dict_race_info["prize_money_4"] == 37.5
    assert dict_race_info["prize_money_5"] == 25.0
    assert dict_race_info["place_id"] == 8


def test_parse_feed():
    s3_feed_url = urlparse(aws_settings["AWS_S3_FEED_URL"])
    s3_feed_path = s3_feed_url.path[1:]

    json_data = crawl_racelist.get_feed(s3_client, s3_feed_path)

    df_race_info = crawl_racelist.parse_feed(json_data)

    assert len(df_race_info) > 0


def test_extract_racelist():
    s3_feed_url = urlparse(aws_settings["AWS_S3_FEED_URL"])
    s3_feed_path = s3_feed_url.path[1:]

    json_data = crawl_racelist.get_feed(s3_client, s3_feed_path)
    df_race_info = crawl_racelist.parse_feed(json_data)

    df_tmp = crawl_racelist.extract_racelist(df_race_info, datetime(2023, 12, 15))
    assert len(df_tmp) > 0

    df_tmp = crawl_racelist.extract_racelist(df_race_info, datetime(2023, 1, 1))
    assert len(df_tmp) == 0
