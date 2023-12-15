from scrapy import Field, Item


class RaceInfoItem(Item):
    """レース情報
    """
    url = Field()
    race_id = Field()
    race_round = Field()
    race_name = Field()
    race_data1 = Field()
    race_data2 = Field()
    race_data3 = Field()


class RaceBracketItem(Item):
    """枠データ
    """
    url = Field()
    race_id = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_url = Field()
    jockey_url = Field()
    jockey_weight = Field()
    trainer_url = Field()
    horse_weight_diff = Field()


class HorseItem(Item):
    """競走馬
    """
    url = Field()
    horse_id = Field()
    horse_name = Field()
    gender_coat_color = Field()
    birthday = Field()
    owner_url = Field()
    owner_name = Field()
    breeder_url = Field()
    breeder_name = Field()
    breeding_farm = Field()


class ParentHorseItem(Item):
    """競走馬血統
    """
    url = Field()
    horse_id = Field()
    parent_horse_url_m = Field()
    parent_horse_url_f = Field()
    parent_horse_url_m_m = Field()
    parent_horse_url_m_f = Field()
    parent_horse_url_f_m = Field()
    parent_horse_url_f_f = Field()
    parent_horse_url_m_m_m = Field()
    parent_horse_url_m_m_f = Field()
    parent_horse_url_m_f_m = Field()
    parent_horse_url_m_f_f = Field()
    parent_horse_url_f_m_m = Field()
    parent_horse_url_f_m_f = Field()
    parent_horse_url_f_f_m = Field()
    parent_horse_url_f_f_f = Field()
    parent_horse_url_m_m_m_m = Field()
    parent_horse_url_m_m_m_f = Field()
    parent_horse_url_m_m_f_m = Field()
    parent_horse_url_m_m_f_f = Field()
    parent_horse_url_m_f_m_m = Field()
    parent_horse_url_m_f_m_f = Field()
    parent_horse_url_m_f_f_m = Field()
    parent_horse_url_m_f_f_f = Field()
    parent_horse_url_f_m_m_m = Field()
    parent_horse_url_f_m_m_f = Field()
    parent_horse_url_f_m_f_m = Field()
    parent_horse_url_f_m_f_f = Field()
    parent_horse_url_f_f_m_m = Field()
    parent_horse_url_f_f_m_f = Field()
    parent_horse_url_f_f_f_m = Field()
    parent_horse_url_f_f_f_f = Field()
    parent_horse_url_m_m_m_m_m = Field()
    parent_horse_url_m_m_m_m_f = Field()
    parent_horse_url_m_m_m_f_m = Field()
    parent_horse_url_m_m_m_f_f = Field()
    parent_horse_url_m_m_f_m_m = Field()
    parent_horse_url_m_m_f_m_f = Field()
    parent_horse_url_m_m_f_f_m = Field()
    parent_horse_url_m_m_f_f_f = Field()
    parent_horse_url_m_f_m_m_m = Field()
    parent_horse_url_m_f_m_m_f = Field()
    parent_horse_url_m_f_m_f_m = Field()
    parent_horse_url_m_f_m_f_f = Field()
    parent_horse_url_m_f_f_m_m = Field()
    parent_horse_url_m_f_f_m_f = Field()
    parent_horse_url_m_f_f_f_m = Field()
    parent_horse_url_m_f_f_f_f = Field()
    parent_horse_url_f_m_m_m_m = Field()
    parent_horse_url_f_m_m_m_f = Field()
    parent_horse_url_f_m_m_f_m = Field()
    parent_horse_url_f_m_m_f_f = Field()
    parent_horse_url_f_m_f_m_m = Field()
    parent_horse_url_f_m_f_m_f = Field()
    parent_horse_url_f_m_f_f_m = Field()
    parent_horse_url_f_m_f_f_f = Field()
    parent_horse_url_f_f_m_m_m = Field()
    parent_horse_url_f_f_m_m_f = Field()
    parent_horse_url_f_f_m_f_m = Field()
    parent_horse_url_f_f_m_f_f = Field()
    parent_horse_url_f_f_f_m_m = Field()
    parent_horse_url_f_f_f_m_f = Field()
    parent_horse_url_f_f_f_f_m = Field()
    parent_horse_url_f_f_f_f_f = Field()


class JockeyItem(Item):
    """騎手
    """
    url = Field()
    jockey_id = Field()
    jockey_name = Field()
    debut_year = Field()


class TrainerItem(Item):
    """調教師
    """
    url = Field()
    trainer_id = Field()
    trainer_name = Field()
    debut_year = Field()


# class OddsWinPlaceItem(Item):
#     """オッズ(単勝・複勝)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number = Field()
#     horse_url = Field()
#     odds_win = Field()
#     odds_place = Field()


# class OddsQuinellaItem(Item):
#     """オッズ(馬連)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number_1 = Field()
#     horse_number_2 = Field()
#     odds = Field()


# class OddsExactaItem(Item):
#     """オッズ(馬単)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number_1 = Field()
#     horse_number_2 = Field()
#     odds = Field()


# class OddsQuinellaPlaceItem(Item):
#     """オッズ(ワイド)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number_1 = Field()
#     horse_number_2 = Field()
#     odds_lower = Field()
#     odds_upper = Field()


# class OddsTrioItem(Item):
#     """オッズ(三連複)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number_1_2 = Field()
#     horse_number_3 = Field()
#     odds = Field()


# class OddsTrifectaItem(Item):
#     """オッズ(三連単)ページ"""
#     item_type = Field()
#     odds_url = Field()
#     horse_number = Field()
#     odds = Field()


class RaceResultItem(Item):
    """レース結果
    """
    url = Field()
    race_id = Field()
    result = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_url = Field()
    arrival_time = Field()
    arrival_margin = Field()
    final_600_meters_time = Field()


class RacePayoffItem(Item):
    """払戻し
    """
    url = Field()
    race_id = Field()
    bet_type = Field()
    horse_number = Field()
    payoff_money = Field()
    favorite_order = Field()


class RaceCornerPassingOrderItem(Item):
    """コーナー通過順位
    """
    url = Field()
    race_id = Field()
    corner_name = Field()
    passing_order = Field()


class RaceLaptimeItem(Item):
    """ラップタイム
    """
    url = Field()
    race_id = Field()
    data = Field()
