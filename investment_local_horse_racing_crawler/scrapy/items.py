# -*- coding: utf-8 -*-


from scrapy import Item, Field


# カレンダー・ページのリンク先
class CalendarItem(Item):
    calendar_url = Field()
    race_list_urls = Field()


# レース情報(ミニ)
class RaceInfoMiniItem(Item):
    race_list_url = Field()
    race_name = Field()
    race_denma_url = Field()
    course_length = Field()
    start_time = Field()


# 出馬ページのレース情報
class RaceInfoItem(Item):
    race_denma_url = Field()
    race_round = Field()
    race_name = Field()
    start_date = Field()
    place_name = Field()
    course_type_length = Field()
    start_time = Field()
    weather_url = Field()
    course_condition = Field()
    moisture = Field()
    prize_money = Field()



# 出馬ページのリスト
class RaceDenmaItem(Item):
    race_denma_url = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_url = Field()
    jockey_url = Field()
    jockey_weight = Field()
    trainer_url = Field()
    odds_win_favorite = Field()
    horse_weight = Field()
    horse_weight_diff = Field()



# 結果ページのリスト
class RaceResultItem(Item):
    race_result_url = Field()
    result = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_url = Field()
    arrival_time = Field()
    arrival_margin = Field()
    final_600_meters_time = Field()
    corner_passing_order = Field()




# 結果ページのコーナー通過順
class RaceCornerPassingOrderItem(Item):
    race_result_url = Field()
    corner_number = Field()
    passing_order = Field()



# 結果ページの払い戻し金
class RaceRefundItem(Item):
    race_result_url = Field()
    betting_type = Field()
    horse_number = Field()
    refund_money = Field()
    favorite = Field()



# 競走馬ページ
class HorseItem(Item):
    horse_url = Field()
    horse_name = Field()
    gender_age = Field()
    birthday = Field()
    coat_color = Field()
    trainer_url = Field()
    owner = Field()
    breeder = Field()
    breeding_farm = Field()
    parent_horse_name_1 = Field()
    parent_horse_name_2 = Field()
    grand_parent_horse_name_1 = Field()
    grand_parent_horse_name_2 = Field()
    grand_parent_horse_name_3 = Field()
    grand_parent_horse_name_4 = Field()




# 騎手ページ
class JockeyItem(Item):
    jockey_url = Field()
    jockey_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()
    trainer_url = Field()
    first_licensing_year = Field()




# 調教師ページ
class TrainerItem(Item):
    trainer_url = Field()
    trainer_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()




# オッズ(単勝・複勝)ページ
class OddsWinPlaceItem(Item):
    odds_url = Field()
    horse_number = Field()
    horse_url = Field()
    odds_win = Field()
    odds_place = Field()



# オッズ・ページからのリンク先
class OddsUrlItem(Item):
    odds_url = Field()
    odds_sub_urls = Field()
