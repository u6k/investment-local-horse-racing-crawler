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
