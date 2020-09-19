# -*- coding: utf-8 -*-


from scrapy import Item, Field


class RaceInfoItem(Item):
    race_id = Field()
    race_round = Field()
    race_name = Field()
    start_date = Field()
    place_name = Field()
    course_type_length = Field()
    start_time = Field()
    weather = Field()
    moisture = Field()
    course_condition = Field()
    added_money = Field()


class RaceDenmaItem(Item):
    race_id = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_id = Field()
    jockey_id = Field()
    jockey_weight = Field()
    trainer_id = Field()
    odds_win = Field()
    favorite = Field()
    horse_weight = Field()
    horse_weight_diff = Field()


class OddsWinPlaceItem(Item):
    race_id = Field()
    horse_number = Field()
    horse_id = Field()
    odds_win = Field()
    odds_place_min = Field()
    odds_place_max = Field()


class RaceResultItem(Item):
    race_id = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_id = Field()
    result = Field()
    arrival_time = Field()
    arrival_margin = Field()
    final_600_meters_time = Field()
    corner_passing_order = Field()


class RacePayoffItem(Item):
    race_id = Field()
    payoff_type = Field()
    horse_number = Field()
    odds = Field()
    favorite = Field()


class HorseItem(Item):
    horse_id = Field()
    horse_name = Field()
    gender_age = Field()
    birthday = Field()
    coat_color = Field()
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
    jockey_id = Field()
    jockey_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()
    first_licensing_year = Field()


class TrainerItem(Item):
    trainer_id = Field()
    trainer_name = Field()
    birthday = Field()
    gender = Field()
    belong_to = Field()
