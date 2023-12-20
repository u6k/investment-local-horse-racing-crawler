import io
import json
import os
import re
import subprocess
import time
from datetime import datetime, timedelta

import pandas as pd

from local_horse_racing_crawler.settings import get_logger

#
# S3操作
#


def get_feed(s3_client, s3_feed_path):
    L = get_logger("get_feed")
    L.info(f"start: s3_feed_path={s3_feed_path}")

    # ダウンロードして、jsonとして読み込む
    with io.BytesIO(s3_client.get_bytes(s3_feed_path)) as b:
        json_data = json.load(b)

    return json_data


def get_racelist(s3_client, s3_racelist_folder, target_date):
    L = get_logger("get_racelist")
    L.info(f"start: s3_racelist_folder={s3_racelist_folder}, target_date={target_date}")

    # ダウンロードする
    s3_key = f"{s3_racelist_folder}/{target_date.strftime('%Y%m%d')}/df_racelist.joblib"
    L.debug(f"s3_key={s3_key}")

    df_racelist = s3_client.get_joblib(s3_key)

    L.debug(df_racelist)

    return df_racelist


def put_racelist(s3_client, df_racelist, s3_racelist_folder, target_date):
    L = get_logger("put_racelist")
    L.info(f"start: len(df_racelist)={len(df_racelist)}, s3_racelist_folder={s3_racelist_folder}, target_date={target_date}")

    # joblibで変換して、アップロードする
    s3_key = f"{s3_racelist_folder}/{target_date.strftime('%Y%m%d')}/df_racelist.joblib"
    L.debug(f"s3_key={s3_key}")

    s3_client.put_joblib(df_racelist, s3_key)

    # csvに変換して、アップロードする
    s3_key = f"{s3_racelist_folder}/{target_date.strftime('%Y%m%d')}/df_racelist.csv"
    L.debug(f"s3_key={s3_key}")

    with io.BytesIO() as b:
        df_racelist.to_csv(b)
        s3_client.put_bytes(b.getvalue(), s3_key)


#
# レースデータ操作
#

def extract_racelist(df_race_info, target_date):
    L = get_logger("extract_racelist")
    L.info(f"start: len(df_race_info)={len(df_race_info)}, target_date={target_date}")

    # レース情報から対象日のデータを抽出する
    start_date = target_date
    end_date = start_date + timedelta(days=1)

    df_race_info = df_race_info.query(f"'{start_date}'<=start_datetime<'{end_date}'").sort_values("start_datetime")

    # n分刻みのレース一覧を生成する
    dict_racelist = {
        "race_id": [],
        "diff_minutes": [],
        "place_id": [],
        "race_round": [],
        "start_datetime": [],
        "crawl_start_datetime": [],
        "crawl_finish_datetime": [],
        "key": [],
    }

    for _, row in df_race_info.iterrows():
        for diff_minutes in [30, 20, 15, 10, 5]:
            dict_racelist["race_id"].append(row["race_id"])
            dict_racelist["place_id"].append(row["place_id"])
            dict_racelist["race_round"].append(row["race_round"])
            dict_racelist["start_datetime"].append(row["start_datetime"])

            dict_racelist["diff_minutes"].append(diff_minutes)
            dict_racelist["crawl_start_datetime"].append(row["start_datetime"] - timedelta(minutes=diff_minutes))
            dict_racelist["crawl_finish_datetime"].append(None)
            dict_racelist["key"].append(f"{row['race_id']}_before_{diff_minutes}minutes")

    df_racelist = pd.DataFrame(dict_racelist) \
        .sort_values(["start_datetime", "crawl_start_datetime"]) \
        .astype({
            "race_id": "str",
            "diff_minutes": "int",
            "place_id": "str",
            "race_round": "int",
            "start_datetime": "datetime64[ns]",
            "crawl_start_datetime": "datetime64[ns]",
            "crawl_finish_datetime": "datetime64[ns]",
        })

    L.debug(df_racelist)

    return df_racelist


race_info_url_pattern = re.compile(r"^https:\/\/nar\.netkeiba\.com\/race\/shutuba\.html\?race_id=([0-9]+)#race_info$")


def parse_feed(json_data):
    L = get_logger("parse_feed")
    L.info("start:")

    list_race_info = []

    # 変換する
    for json_item in json_data:
        if race_info_url_pattern.fullmatch(json_item["url"][0]) is not None:
            list_race_info.append(parse_race_info(json_item))

        else:
            pass

    # データフレーム化する
    df_race_info = pd.DataFrame(list_race_info) \
        .drop_duplicates(subset=["race_id"]) \
        .sort_values(["start_datetime"]) \
        .reset_index(drop=True)

    L.debug(df_race_info)

    return df_race_info


race_round_pattern = re.compile(r"^([0-9]+)R$")
start_time_pattern = re.compile(r"([0-9]+):([0-9]+)発走")
course_type_pattern = re.compile(r"(芝|ダ)([0-9]+)m \((\w+)\)")
weather_pattern = re.compile(r"天候:(.)")
course_condition_pattern = re.compile(r"馬場:(.)")
prize_money_pattern = re.compile(r"本賞金:([0-9\.]+)、([0-9\.]+)、([0-9\.]+)、([0-9\.]+)、([0-9\.]+)万円")
start_date_pattern = re.compile(r"([0-9]+)年([0-9]+)月([0-9]+)日")
place_pattern = re.compile(r"(\w+?)[0-9]+R")

course_type_table = {
    "芝": 1,
    "ダ": 2,
}

weather_table = {
    "晴": 1,
    "曇": 2,
    "雨": 3,
}

course_condition_table = {
    "良": 1,
    "稍": 2,
    "重": 3,
    "不": 4,
}

place_table = {
    "帯広": 1,
    "門別": 2,
    "盛岡": 3,
    "水沢": 4,
    "浦和": 5,
    "船橋": 6,
    "大井": 7,
    "川崎": 8,
    "金沢": 9,
    "笠松": 10,
    "名古屋": 11,
    "園田": 12,
    "姫路": 13,
    "高知": 14,
    "佐賀": 15,
}


def parse_race_info(json_item):
    race_round_re = race_round_pattern.fullmatch(json_item["race_round"][0])
    start_time_re = start_time_pattern.search(json_item["race_data1"][0])
    course_type_re = course_type_pattern.search(json_item["race_data1"][0])
    weather_re = weather_pattern.search(json_item["race_data1"][0])
    course_condition_re = course_condition_pattern.search(json_item["race_data1"][0])
    prize_money_re = prize_money_pattern.search(json_item["race_data2"][0])
    start_date_re = start_date_pattern.search(json_item["race_data3"][0])
    place_re = place_pattern.search(json_item["race_data3"][0])

    result = {
        "race_id": json_item["race_id"][0],
        "race_round": int(race_round_re.group(1)),
        "race_name": json_item["race_name"][0],
        "start_datetime": datetime(int(start_date_re.group(1)), int(start_date_re.group(2)), int(start_date_re.group(3)), int(start_time_re.group(1)), int(start_time_re.group(2)), 0),
        "course_type_id": course_type_table[course_type_re.group(1)],
        "course_length": int(course_type_re.group(2)),
        "course_curve": course_type_re.group(3),
        "weather_id": weather_table[weather_re.group(1)],
        "course_condition": course_condition_table[course_condition_re.group(1)],
        "prize_money_1": float(prize_money_re.group(1)),
        "prize_money_2": float(prize_money_re.group(2)),
        "prize_money_3": float(prize_money_re.group(3)),
        "prize_money_4": float(prize_money_re.group(4)),
        "prize_money_5": float(prize_money_re.group(5)),
        "place_id": place_table[place_re.group(1)],
    }

    return result


def find_target_racelist(df_racelist, now_datetime):
    """
    まだクロールしていない、クロール開始時刻に到達したレースを抽出する
    """
    L = get_logger("extract_not_crawl_racelist")
    L.debug(f"start: now_datetime={now_datetime}")

    # クロールが終了していない、かつ、クロール開始時刻に到達したレースを抽出する
    df_result = df_racelist.query(f"crawl_finish_datetime.isnull() and crawl_start_datetime<='{now_datetime}'")

    return df_result


def crawl_race_in_subprocess(df_racelist, crawl_queue, queue_count):
    """
    サブプロセスでクロールを実行する
    """
    L = get_logger("crawl_race_in_subprocess")
    L.info(f"start: len(df_racelist)={len(df_racelist)}, len(crawl_queue)={len(crawl_queue)}, queue_count={queue_count}")

    for race_item in df_racelist.to_dict(orient="records"):
        L.debug(f"race_item={race_item}")

        if len(crawl_queue) >= queue_count:
            # 既にキューが埋まっている場合、ループを抜ける
            break

        if race_item["key"] in crawl_queue:
            # キューに既に存在する場合、スキップする
            continue

        # クロールのパラメーターを構築する
        start_url = f"https://nar.netkeiba.com/race/shutuba.html?race_id={race_item['race_id']}"

        env = os.environ.copy()
        env["AWS_S3_FEED_URL"] = f"s3://{env['AWS_S3_CACHE_BUCKET']}/{env['AWS_S3_RACELIST_FOLDER']}/{race_item['start_datetime'].strftime('%Y%m%d')}/race_{race_item['race_id']}_before_{race_item['diff_minutes']}minutes.json"
        env["RECACHE_RACE"] = "True"
        env["RECACHE_DATA"] = "False"

        L.debug(f"start_url={start_url}")
        L.debug(f"env={env}")

        # クロールプロセスを起動する
        proc = start_subprocess(start_url, env)

        # キューに追加する
        race_item["proc"] = proc
        crawl_queue[race_item["key"]] = race_item

    L.debug(f"crawl_queue={list(crawl_queue.keys())}")

    return crawl_queue


def start_subprocess(start_url, env):
    """
    サブプロセスを起動する(モック用)
    """

    proc = subprocess.Popen(["scrapy", "crawl", "netkeiba_spider", "-a", f"start_url={start_url}"], env=env)

    # NOTE: テスト時にコメントインする
    # class MockCrawlSubprocess:
    #     def __init__(self, start_url, env):
    #         self.start_url = start_url
    #         self.env = env

    #     def poll(self):
    #         return 0

    # proc = MockCrawlSubprocess(start_url, env)

    return proc


def find_crawl_finished_race_items(crawl_queue):
    """
    クロールが終了したレース情報を返す
    """
    L = get_logger("find_crawl_finished_race_items")
    L.info("start:")

    # サブプロセスが終了しているか確認し、終了しているレース情報を取得する
    result = []

    for race_item in crawl_queue.values():
        if race_item["proc"].poll() is not None:
            L.debug(f"クロール終了: {race_item}")

            result.append(race_item)

    L.debug(result)

    return result


def update_racelist(s3_client, race_items, now_datetime, df_racelist, crawl_queue, s3_racelist_folder, target_date):
    """
    クロールが終了したレース情報について、レース一覧を更新・アップロードして、キューから削除する
    """
    L = get_logger("update_racelist")
    L.info(f"start: len(race_items)={len(race_items)}, len(df_racelist)={len(df_racelist)}, len(crawl_queue)={len(crawl_queue)}, s3_racelist_folder={s3_racelist_folder}, target_date={target_date}")

    # レース一覧を更新し、キューから削除する
    for race_item in race_items:
        df_racelist.loc[df_racelist["key"] == race_item["key"], "crawl_finish_datetime"] = now_datetime

        del crawl_queue[race_item["key"]]

    # 更新したレース一覧をアップロードする
    put_racelist(s3_client, df_racelist, s3_racelist_folder, target_date)

    return df_racelist, crawl_queue


def find_crawl_unfinished_racelist(df_racelist):
    """
    クロールが終了していないレース一覧を取得する
    """
    L = get_logger("find_crawl_unfinished_racelist")
    L.info("start")

    # クロールが終了していないレース一覧を取得する
    df_result = df_racelist.query("crawl_finish_datetime.isnull()")

    L.debug(df_result)

    return df_result


#
# メイン処理
#

def create_racelist(s3_client, s3_feed_path, target_date, s3_racelist_folder):
    L = get_logger("create_racelist")
    L.info(f"start: s3_feed_path={s3_feed_path}, target_date={target_date}, s3_racelist_folder={s3_racelist_folder}")

    # フィードをダウンロードする
    json_data = get_feed(s3_client, s3_feed_path)

    # フィードを変換する
    df_race_info = parse_feed(json_data)

    # レース一覧を抽出する
    df_racelist = extract_racelist(df_race_info, target_date)

    # レース一覧をアップロードする
    put_racelist(s3_client, df_racelist, s3_racelist_folder, target_date)


def crawl_race(s3_client, s3_racelist_folder, target_date, queue_count):
    L = get_logger("crawl_race")
    L.debug(f"start: s3_racelist_folder={s3_racelist_folder}, target_date={target_date}, queue_count={queue_count}")

    # レース一覧を読み込む
    df_racelist = get_racelist(s3_client, s3_racelist_folder, target_date)

    crawl_queue = {}

    while True:
        # まだクロールしていない、クロール開始時刻に到達したレースを抽出する
        df_target_racelist = find_target_racelist(df_racelist, datetime.now())

        # キューに存在しない対象レースを、サブプロセスでクロールする
        crawl_queue = crawl_race_in_subprocess(df_target_racelist, crawl_queue, queue_count)

        # クロール結果を確認する
        finished_race_items = find_crawl_finished_race_items(crawl_queue)

        if len(finished_race_items) > 0:
            # クロールが終了している場合、レース一覧を更新・アップロードして、キューから削除する
            df_racelist, crawl_queue = update_racelist(s3_client, finished_race_items, datetime.now(), df_racelist, crawl_queue, s3_racelist_folder, target_date)

        # 全レースのクロールが終了した場合、ループを終了する
        df_unfinished_racelist = find_crawl_unfinished_racelist(df_racelist)

        if len(df_unfinished_racelist) == 0:
            L.debug("全てのクロールが終了したので、ループを抜ける")
            break

        time.sleep(1)
