import re

from scrapy.contracts import Contract
from scrapy.http import Request

from local_horse_racing_crawler.items import HorseItem, JockeyItem, OddsItem, ParentHorseItem, RaceBracketItem, RaceCornerPassingOrderItem, RaceInfoItem, RaceLaptimeItem, RacePayoffItem, RaceResultItem, TrainerItem


class CalendarContract(Contract):
    name = "calendar_contract"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        race_list_url_re = re.compile(r"^https:\/\/nar\.netkeiba\.com\/top\/race_list_sub\.html\?kaisai_date=[0-9]{8}$")
        race_list_requests = [r for r in requests if race_list_url_re.fullmatch(r.url) is not None]

        assert len(race_list_requests) == 112


class RaceListContract(Contract):
    name = "race_list_contract"

    def post_process(self, output):
        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        race_shutuba_url_re = re.compile(r"^https:\/\/nar\.netkeiba\.com\/race\/shutuba\.html\?race_id=[0-9]+$")
        race_shutuba_requests = [r for r in requests if race_shutuba_url_re.fullmatch(r.url) is not None]

        assert len(race_shutuba_requests) == 58


class RaceProgramContract(Contract):
    name = "race_program_contract"

    def post_process(self, output):
        #
        # Check items
        #

        # レース情報
        items = [o for o in output if isinstance(o, RaceInfoItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_info"]
        assert i["race_id"] == ["202344111410"]
        assert i["race_round"] == ["10R"]
        assert i["race_name"] == ["八潮パークタウン40周年特別競走(B2)"]
        assert i["race_data1"] == ["19:30発走 / ダ1200m (右) / 天候:晴 / 馬場:良 \xa0"]
        assert i["race_data2"] == ["13回 大井 2日目 サラ系一般 B2 \xa0\xa0\xa0\xa0\xa0 16頭 本賞金:270.0、108.0、67.5、40.5、27.0万円"]
        assert i["race_data3"] == ["八潮パークタウン40 出馬表 | 2023年11月14日 大井10R 地方競馬レース情報 - netkeiba.com"]

        # 枠データ
        items = [o for o in output if isinstance(o, RaceBracketItem)]

        assert len(items) == 16

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["1"]
        assert i["horse_number"] == ["1"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2017103463"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05590"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05655"]
        assert i["horse_weight_diff"] == ["508(-1)"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["1"]
        assert i["horse_number"] == ["2"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103331"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05554"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05722"]
        assert i["horse_weight_diff"] == ["498(+8)"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["15"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103916"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05443"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05769"]
        assert i["horse_weight_diff"] == ["486(+10)"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/race/shutuba.html?race_id=202344111410#race_bracket"]
        assert i["race_id"] == ["202344111410"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["16"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2016101473"]
        assert i["jockey_url"] == ["https://db.netkeiba.com/jockey/result/recent/05411"]
        assert i["jockey_weight"] == ["56.0"]
        assert i["trainer_url"] == ["https://db.netkeiba.com/trainer/result/recent/05655"]
        assert i["horse_weight_diff"] == ["470(+6)"]

        #
        # Check requests
        #

        requests = [o for o in output if isinstance(o, Request)]

        horse_url_re = re.compile(r"^https:\/\/db\.netkeiba\.com\/horse\/[a-z0-9]+\/?$")
        horse_requests = [r for r in requests if horse_url_re.fullmatch(r.url) is not None]

        assert len(horse_requests) == 16

        jockey_url_re = re.compile(r"^https:\/\/db\.netkeiba\.com\/jockey/[a-z0-9]+\/?$")
        jockey_requests = [r for r in requests if jockey_url_re.fullmatch(r.url) is not None]

        assert len(jockey_requests) == 16

        trainer_url_re = re.compile(r"^https:\/\/db\.netkeiba\.com\/trainer\/[a-z0-9]+\/?$")
        trainer_requests = [r for r in requests if trainer_url_re.fullmatch(r.url) is not None]

        assert len(trainer_requests) == 16

        odds_url_re = re.compile(r"^https:\/\/nar\.netkeiba\.com\/odds\/odds_get_form.html\?type=b[0-9]&race_id=[0-9]+(&jiku=[0-9]+)?$")
        odds_requests = [r for r in requests if odds_url_re.fullmatch(r.url) is not None]
        assert len(odds_requests) == 36

        result_url_re = re.compile(r"^https:\/\/nar\.netkeiba\.com\/race\/result\.html\?race_id=[0-9]+$")
        result_requests = [r for r in requests if result_url_re.fullmatch(r.url)]

        assert len(result_requests) == 1


class HorseContract(Contract):
    name = "horse_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, HorseItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://db.netkeiba.com/horse/2017103463"]
        assert i["horse_id"] == ["2017103463"]
        assert i["horse_name"] == ["ドーロカグラ"]
        assert i["gender_coat_color"] == ["\u3000牡\u3000黒鹿毛"]
        assert i["birthday"] == ["2017年5月9日"]
        assert i["owner_url"] == ["https://db.netkeiba.com/owner/x076d0/"]
        assert i["owner_name"] == ["曽根正"]
        assert i["breeder_url"] == ["https://db.netkeiba.com/breeder/704079/"]
        assert i["breeder_name"] == ["グランド牧場"]
        assert i["breeding_farm"] == ["新ひだか町"]

        # Check requests
        requests = [o for o in output if isinstance(o, Request)]

        parent_horse_url_re = re.compile(r"^https:\/\/db\.netkeiba\.com\/horse\/ped\/[a-z0-9]+\/?$")
        parent_requests = [r for r in requests if parent_horse_url_re.fullmatch(r.url) is not None]

        assert len(parent_requests) == 1


class ParentHorseContract(Contract):
    name = "parent_horse_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, ParentHorseItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://db.netkeiba.com/horse/ped/2017103463/"]
        assert i["horse_id"] == ["2017103463"]
        assert i["parent_horse_url_m"] == ["https://db.netkeiba.com/horse/2009110009/"]
        assert i["parent_horse_url_f"] == ["https://db.netkeiba.com/horse/2011101929/"]
        assert i["parent_horse_url_m_m"] == ["https://db.netkeiba.com/horse/000a010a65/"]
        assert i["parent_horse_url_m_f"] == ["https://db.netkeiba.com/horse/1997102034/"]
        assert i["parent_horse_url_f_m"] == ["https://db.netkeiba.com/horse/2007110008/"]
        assert i["parent_horse_url_f_f"] == ["https://db.netkeiba.com/horse/1999100314/"]
        assert i["parent_horse_url_m_m_m"] == ["https://db.netkeiba.com/horse/000a001fb5/"]
        assert i["parent_horse_url_m_m_f"] == ["https://db.netkeiba.com/horse/000a010a72/"]
        assert i["parent_horse_url_m_f_m"] == ["https://db.netkeiba.com/horse/000a000013/"]
        assert i["parent_horse_url_m_f_f"] == ["https://db.netkeiba.com/horse/1989107125/"]
        assert i["parent_horse_url_f_m_m"] == ["https://db.netkeiba.com/horse/000a010dc8/"]
        assert i["parent_horse_url_f_m_f"] == ["https://db.netkeiba.com/horse/1999100306/"]
        assert i["parent_horse_url_f_f_m"] == ["https://db.netkeiba.com/horse/1988109110/"]
        assert i["parent_horse_url_f_f_f"] == ["https://db.netkeiba.com/horse/000a0061c1/"]
        assert i["parent_horse_url_m_m_m_m"] == ["https://db.netkeiba.com/horse/000a00185d/"]
        assert i["parent_horse_url_m_m_m_f"] == ["https://db.netkeiba.com/horse/000a00940f/"]
        assert i["parent_horse_url_m_m_f_m"] == ["https://db.netkeiba.com/horse/000a001907/"]
        assert i["parent_horse_url_m_m_f_f"] == ["https://db.netkeiba.com/horse/000a010a71/"]
        assert i["parent_horse_url_m_f_m_m"] == ["https://db.netkeiba.com/horse/000a001607/"]
        assert i["parent_horse_url_m_f_m_f"] == ["https://db.netkeiba.com/horse/000a009232/"]
        assert i["parent_horse_url_m_f_f_m"] == ["https://db.netkeiba.com/horse/000a0016eb/"]
        assert i["parent_horse_url_m_f_f_f"] == ["https://db.netkeiba.com/horse/000a0002c5/"]
        assert i["parent_horse_url_f_m_m_m"] == ["https://db.netkeiba.com/horse/000a010a96/"]
        assert i["parent_horse_url_f_m_m_f"] == ["https://db.netkeiba.com/horse/000a010e19/"]
        assert i["parent_horse_url_f_m_f_m"] == ["https://db.netkeiba.com/horse/1985109002/"]
        assert i["parent_horse_url_f_m_f_f"] == ["https://db.netkeiba.com/horse/1984100409/"]
        assert i["parent_horse_url_f_f_m_m"] == ["https://db.netkeiba.com/horse/000a0017b0/"]
        assert i["parent_horse_url_f_f_m_f"] == ["https://db.netkeiba.com/horse/000a00977a/"]
        assert i["parent_horse_url_f_f_f_m"] == ["https://db.netkeiba.com/horse/000a0010fa/"]
        assert i["parent_horse_url_f_f_f_f"] == ["https://db.netkeiba.com/horse/000a00890e/"]
        assert i["parent_horse_url_m_m_m_m_m"] == ["https://db.netkeiba.com/horse/000a000e04/"]
        assert i["parent_horse_url_m_m_m_m_f"] == ["https://db.netkeiba.com/horse/000a008892/"]
        assert i["parent_horse_url_m_m_m_f_m"] == ["https://db.netkeiba.com/horse/000a000dd9/"]
        assert i["parent_horse_url_m_m_m_f_f"] == ["https://db.netkeiba.com/horse/000a0081b6/"]
        assert i["parent_horse_url_m_m_f_m_m"] == ["https://db.netkeiba.com/horse/000a0010a8/"]
        assert i["parent_horse_url_m_m_f_m_f"] == ["https://db.netkeiba.com/horse/000a008740/"]
        assert i["parent_horse_url_m_m_f_f_m"] == ["https://db.netkeiba.com/horse/000a000ddb/"]
        assert i["parent_horse_url_m_m_f_f_f"] == ["https://db.netkeiba.com/horse/000a00ad62/"]
        assert i["parent_horse_url_m_f_m_m_m"] == ["https://db.netkeiba.com/horse/000a000e46/"]
        assert i["parent_horse_url_m_f_m_m_f"] == ["https://db.netkeiba.com/horse/000a007e0c/"]
        assert i["parent_horse_url_m_f_m_f_m"] == ["https://db.netkeiba.com/horse/000a001bd8/"]
        assert i["parent_horse_url_m_f_m_f_f"] == ["https://db.netkeiba.com/horse/000a009231/"]
        assert i["parent_horse_url_m_f_f_m_m"] == ["https://db.netkeiba.com/horse/000a000dfe/"]
        assert i["parent_horse_url_m_f_f_m_f"] == ["https://db.netkeiba.com/horse/000a0083a6/"]
        assert i["parent_horse_url_m_f_f_f_m"] == ["https://db.netkeiba.com/horse/000a001343/"]
        assert i["parent_horse_url_m_f_f_f_f"] == ["https://db.netkeiba.com/horse/000a0084ec/"]
        assert i["parent_horse_url_f_m_m_m_m"] == ["https://db.netkeiba.com/horse/000a000013/"]
        assert i["parent_horse_url_f_m_m_m_f"] == ["https://db.netkeiba.com/horse/000a010ab2/"]
        assert i["parent_horse_url_f_m_m_f_m"] == ["https://db.netkeiba.com/horse/1986109000/"]
        assert i["parent_horse_url_f_m_m_f_f"] == ["https://db.netkeiba.com/horse/000a010e18/"]
        assert i["parent_horse_url_f_m_f_m_m"] == ["https://db.netkeiba.com/horse/000a00193a/"]
        assert i["parent_horse_url_f_m_f_m_f"] == ["https://db.netkeiba.com/horse/000a008d39/"]
        assert i["parent_horse_url_f_m_f_f_m"] == ["https://db.netkeiba.com/horse/000a0003f6/"]
        assert i["parent_horse_url_f_m_f_f_f"] == ["https://db.netkeiba.com/horse/1955105352/"]
        assert i["parent_horse_url_f_f_m_m_m"] == ["https://db.netkeiba.com/horse/000a001607/"]
        assert i["parent_horse_url_f_f_m_m_f"] == ["https://db.netkeiba.com/horse/000a0081ee/"]
        assert i["parent_horse_url_f_f_m_f_m"] == ["https://db.netkeiba.com/horse/000a000de7/"]
        assert i["parent_horse_url_f_f_m_f_f"] == ["https://db.netkeiba.com/horse/000a009779/"]
        assert i["parent_horse_url_f_f_f_m_m"] == ["https://db.netkeiba.com/horse/000a000e94/"]
        assert i["parent_horse_url_f_f_f_m_f"] == ["https://db.netkeiba.com/horse/000a007cd4/"]
        assert i["parent_horse_url_f_f_f_f_m"] == ["https://db.netkeiba.com/horse/000a000407/"]
        assert i["parent_horse_url_f_f_f_f_f"] == ["https://db.netkeiba.com/horse/000a007237/"]


class JockeyContract(Contract):
    name = "jockey_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, JockeyItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://db.netkeiba.com/jockey/05590"]
        assert i["jockey_id"] == ["05590"]
        assert i["jockey_name"] == ["藤本現暉\xa0 (フジモトゲンキ)"]
        assert i["debut_year"] == ["2015年(9年目)"]


class TrainerContract(Contract):
    name = "trainer_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, TrainerItem)]

        assert len(items) == 1

        i = items[0]
        assert i["url"] == ["https://db.netkeiba.com/trainer/05655"]
        assert i["trainer_id"] == ["05655"]
        assert i["trainer_name"] == ["蛯名雄太\xa0 (エビナユウタ)"]
        assert i["debut_year"] == ["2010年(14年目)"]


class OddsWinPlaceContract(Contract):
    name = "odds_win_place_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 32

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#win"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["16.2"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#win"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["138.3"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#win"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["15"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["138.6"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#win"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["16"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["135.3"]

        i = items[16]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#place"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["2.3 - 4.0"]

        i = items[17]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#place"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["15.3 - 30.3"]

        i = items[30]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#place"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["15"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["12.3 - 24.1"]

        i = items[31]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b1&race_id=202344111410#place"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["16"]
        assert i["horse_number_2"] == [""]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["12.0 - 23.5"]


class OddsExactaContract(Contract):
    name = "odds_exacta_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 240

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["2"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["858.1"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["313.3"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["1149.8"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["1246.6"]

        i = items[238]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["16"]
        assert i["horse_number_2"] == ["14"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["2322.1"]

        i = items[239]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b6&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["16"]
        assert i["horse_number_2"] == ["15"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["4737.1"]


class OddsQuinellaContract(Contract):
    name = "odds_quinella_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 120

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["2"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["461.2"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["145.3"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["437.0"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["348.8"]

        i = items[104]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["10"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["4046.1"]

        i = items[105]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["11"]
        assert i["horse_number_2"] == ["12"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["4.4"]

        i = items[119]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b4&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["15"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["1430.4"]


class OddsQuinellaPlaceContract(Contract):
    name = "odds_quinella_place_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 120

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["2"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["91.6 - 99.2"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["26.6 - 29.5"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["1"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["93.5 - 101.1"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["65.5 - 68.0"]

        i = items[74]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["6"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["255.3 - 264.4"]

        i = items[75]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["7"]
        assert i["horse_number_2"] == ["8"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["164.7 - 171.1"]

        i = items[119]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b5&race_id=202344111410"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["15"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == [""]
        assert i["odds"] == ["298.7 - 302.2"]


class OddsTrifectaContract(Contract):
    name = "odds_trifecta_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 210

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410&jiku=2"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["3"]
        assert i["odds"] == ["12643.4"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410&jiku=2"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["4"]
        assert i["odds"] == ["46683.4"]

        i = items[13]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410&jiku=2"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["16"]
        assert i["odds"] == ["67431.6"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410&jiku=2"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["3"]
        assert i["horse_number_3"] == ["1"]
        assert i["odds"] == ["12912.4"]

        i = items[209]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b8&race_id=202344111410&jiku=2"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["2"]
        assert i["horse_number_2"] == ["16"]
        assert i["horse_number_3"] == ["15"]
        assert i["odds"] == ["303442.5"]


class OddsTrioContract(Contract):
    name = "odds_trio_contract"

    def post_process(self, output):
        # Check item
        items = [o for o in output if isinstance(o, OddsItem)]

        assert len(items) == 105

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["2"]
        assert i["odds"] == ["993.2"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["4"]
        assert i["odds"] == ["1479.1"]

        i = items[13]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["1"]
        assert i["horse_number_3"] == ["16"]
        assert i["odds"] == ["3666.4"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["2"]
        assert i["horse_number_3"] == ["4"]
        assert i["odds"] == ["4152.3"]

        i = items[94]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["11"]
        assert i["horse_number_3"] == ["16"]
        assert i["odds"] == ["2971.0"]

        i = items[95]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["12"]
        assert i["horse_number_3"] == ["13"]
        assert i["odds"] == ["344.9"]

        i = items[104]
        assert i["url"] == ["https://nar.netkeiba.com/odds/odds_get_form.html?type=b7&race_id=202344111410&jiku=3"]
        assert i["race_id"] == ["202344111410"]
        assert i["horse_number_1"] == ["3"]
        assert i["horse_number_2"] == ["15"]
        assert i["horse_number_3"] == ["16"]
        assert i["odds"] == ["14984.5"]


class RaceResultContract(Contract):
    name = "race_result_contract"

    def post_process(self, output):
        #
        # Check items
        #

        # レース結果
        items = [o for o in output if isinstance(o, RaceResultItem)]

        assert len(items) == 16

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["1"]
        assert i["bracket_number"] == ["6"]
        assert i["horse_number"] == ["12"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018101222/"]
        assert i["arrival_time"] == ["1:13.9"]
        assert i["arrival_margin"] == [""]
        assert i["final_600_meters_time"] == ["37.8"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["2"]
        assert i["bracket_number"] == ["7"]
        assert i["horse_number"] == ["14"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018102660/"]
        assert i["arrival_time"] == ["1:14.3"]
        assert i["arrival_margin"] == ["2"]
        assert i["final_600_meters_time"] == ["37.9"]

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["3"]
        assert i["bracket_number"] == ["6"]
        assert i["horse_number"] == ["11"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2019106574/"]
        assert i["arrival_time"] == ["1:14.3"]
        assert i["arrival_margin"] == ["アタマ"]
        assert i["final_600_meters_time"] == ["38.3"]

        i = items[14]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["15"]
        assert i["bracket_number"] == ["8"]
        assert i["horse_number"] == ["15"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2018103916/"]
        assert i["arrival_time"] == ["1:16.5"]
        assert i["arrival_margin"] == ["3"]
        assert i["final_600_meters_time"] == ["39.5"]

        i = items[15]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_result"]
        assert i["race_id"] == ["202344111410"]
        assert i["result"] == ["16"]
        assert i["bracket_number"] == ["5"]
        assert i["horse_number"] == ["10"]
        assert i["horse_url"] == ["https://db.netkeiba.com/horse/2019102218/"]
        assert i["arrival_time"] == ["1:17.6"]
        assert i["arrival_margin"] == ["5"]
        assert i["final_600_meters_time"] == ["41.6"]

        # 払戻しデータ
        items = [o for o in output if isinstance(o, RacePayoffItem)]

        assert len(items) == 9

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["単勝"]
        assert i["horse_number"] == ["12"]
        assert i["payoff_money"] == ["150円"]
        assert i["favorite_order"] == ["1人気"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["複勝"]
        assert i["horse_number"] == ["12 14 11"]
        assert i["payoff_money"] == ["100円170円150円"]
        assert i["favorite_order"] == ["1人気3人気2人気"]

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["枠連"]
        assert i["horse_number"] == ["6 7"]
        assert i["payoff_money"] == ["580円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[3]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["馬連"]
        assert i["horse_number"] == ["12 14"]
        assert i["payoff_money"] == ["740円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[4]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["ワイド"]
        assert i["horse_number"] == ["12 14 11 12 11 14"]
        assert i["payoff_money"] == ["320円240円790円"]
        assert i["favorite_order"] == ["2人気1人気9人気"]

        i = items[5]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["枠単"]
        assert i["horse_number"] == ["6 7"]
        assert i["payoff_money"] == ["670円"]
        assert i["favorite_order"] == ["3人気"]

        i = items[6]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["馬単"]
        assert i["horse_number"] == ["12 14"]
        assert i["payoff_money"] == ["890円"]
        assert i["favorite_order"] == ["2人気"]

        i = items[7]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["3連複"]
        assert i["horse_number"] == ["11 12 14"]
        assert i["payoff_money"] == ["1,170円"]
        assert i["favorite_order"] == ["1人気"]

        i = items[8]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_payoff"]
        assert i["race_id"] == ["202344111410"]
        assert i["bet_type"] == ["3連単"]
        assert i["horse_number"] == ["12 14 11"]
        assert i["payoff_money"] == ["3,240円"]
        assert i["favorite_order"] == ["3人気"]

        # コーナー通過順位データ
        items = [o for o in output if isinstance(o, RaceCornerPassingOrderItem)]

        assert len(items) == 2

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_corner_passing_order"]
        assert i["race_id"] == ["202344111410"]
        assert i["corner_name"] == ["3コーナー"]
        assert i["passing_order"] == ["(10,11),12,13,14,1,16,15,9,6,3,2,8,5,7,4"]

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_corner_passing_order"]
        assert i["race_id"] == ["202344111410"]
        assert i["corner_name"] == ["4コーナー"]
        assert i["passing_order"] == ["11,12,10,(1,14,13),16,9,3,6,15,2,8,5,7,4"]

        # ラップタイムデータ
        items = [o for o in output if isinstance(o, RaceLaptimeItem)]

        assert len(items) == 3

        i = items[0]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['200m', '400m', '600m', '800m', '1000m', '1200m']

        i = items[1]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['12.7', '24.0', '36.0', '48.6', '1:00.7', '1:13.9']

        i = items[2]
        assert i["url"] == ["https://nar.netkeiba.com/race/result.html?race_id=202344111410#race_laptime"]
        assert i["race_id"] == ["202344111410"]
        assert i["data"] == ['12.7', '11.3', '12.0', '12.6', '12.1', '13.2']
