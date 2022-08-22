from scrapy import Field, Item


class CalendarItem(Item):
    """カレンダー・ページのリンク先"""
    item_type = Field()
    calendar_url = Field()
    race_list_urls = Field()


class RaceInfoMiniItem(Item):
    """レース情報(ミニ)"""
    item_type = Field()
    race_list_url = Field()
    race_name = Field()
    race_denma_url = Field()
    course_length = Field()
    start_time = Field()


class RaceInfoItem(Item):
    """出馬ページのレース情報"""
    item_type = Field()
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


class RaceDenmaItem(Item):
    """出馬ページのリスト"""
    item_type = Field()
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


class RaceResultItem(Item):
    """結果ページのリスト"""
    item_type = Field()
    race_result_url = Field()
    result = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_url = Field()
    arrival_time = Field()
    arrival_margin = Field()
    final_600_meters_time = Field()
    corner_passing_order = Field()


class RaceCornerPassingOrderItem(Item):
    """結果ページのコーナー通過順"""
    item_type = Field()
    race_result_url = Field()
    corner_number = Field()
    passing_order = Field()


class RaceRefundItem(Item):
    """結果ページの払い戻し金"""
    item_type = Field()
    race_result_url = Field()
    betting_type = Field()
    horse_number = Field()
    refund_money = Field()
    favorite = Field()


class HorseItem(Item):
    """競走馬ページ"""
    item_type = Field()
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


class JockeyItem(Item):
    """騎手ページ"""
    item_type = Field()
    jockey_url = Field()
    jockey_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()
    trainer_url = Field()
    first_licensing_year = Field()


class TrainerItem(Item):
    """調教師ページ"""
    item_type = Field()
    trainer_url = Field()
    trainer_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()


class OddsWinPlaceItem(Item):
    """オッズ(単勝・複勝)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number = Field()
    horse_url = Field()
    odds_win = Field()
    odds_place = Field()


class OddsQuinellaItem(Item):
    """オッズ(馬連)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds = Field()


class OddsExactaItem(Item):
    """オッズ(馬単)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds = Field()


class OddsQuinellaPlaceItem(Item):
    """オッズ(ワイド)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds_lower = Field()
    odds_upper = Field()


class OddsTrioItem(Item):
    """オッズ(三連複)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number_1_2 = Field()
    horse_number_3 = Field()
    odds = Field()


class OddsTrifectaItem(Item):
    """オッズ(三連単)ページ"""
    item_type = Field()
    odds_url = Field()
    horse_number = Field()
    odds = Field()