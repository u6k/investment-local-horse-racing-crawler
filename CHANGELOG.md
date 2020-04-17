# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unrelease]
### Fixed
- [#8249: カレンダー上の当日レースは、RaceRefundではなくOneDayRaceListにリンクされるため、当日レースが取得できていない](https://redmine.u6k.me/issues/8249)
- [#8187: 払い戻し情報のパースに失敗した…人気がハイフン](https://redmine.u6k.me/issues/8187)
- [#8186: 出馬表のパースに失敗した…単勝オッズが空](https://redmine.u6k.me/issues/8186)

### Added
- [#8166: キャッシュ有効期限をページによって変える](https://redmine.u6k.me/issues/8166)
- [#8171: 外部からジョブを予約実行できるようにする](https://redmine.u6k.me/issues/8171)
- [#8184: 毎日10:00にクロールを開始して、当日の全レース情報を取得して、投票処理を予約実行する](https://redmine.u6k.me/issues/8184)

## [1.0.3] - 2020-04-09
### Fixed
- [#8148: 出馬表のパースに失敗した…馬体重などが空](https://redmine.u6k.me/issues/8148)
- [#8149: オッズ情報のパースが失敗した…単勝オッズがない](https://redmine.u6k.me/issues/8149)
- [#8150: オッズ情報のパースに失敗した…単勝オッズはあるが複勝オッズがない](https://redmine.u6k.me/issues/8150)
- [#8151: レース情報のパースに失敗した…天気データがない](https://redmine.u6k.me/issues/8151)

## [1.0.2] - 2020-04-03
### Fixed
- [#8139: レース払い戻し情報のパースに失敗した](https://redmine.u6k.me/issues/8139)
- [#8140: レース情報のパースに失敗した…水分量のキーが見つからない](https://redmine.u6k.me/issues/8140)
- [#8141: レース出馬表のパースに失敗した…馬体重差を数値にパースできない](https://redmine.u6k.me/issues/8141)
- [#8142: レース出馬表のパースに失敗した…騎手体重が数値に変換できなかった](https://redmine.u6k.me/issues/8142)
- [#8143: レース出馬表のパースに失敗した…オッズがない](https://redmine.u6k.me/issues/8143)
- [#8144: 競走馬ページのパースに失敗した…オーナーがない](https://redmine.u6k.me/issues/8144)
- [#8145: レース結果のパースに失敗した…着順がハイフン](https://redmine.u6k.me/issues/8145)
- [#8146: レース払い戻し情報のパースに失敗した…horse_numberやfavoriteがハイフン](https://redmine.u6k.me/issues/8146)

## [1.0.1] - 2020-04-02
### Fixed
- [#8138: データがDBに格納されない](https://redmine.u6k.me/issues/8138)

## [1.0.0] - 2020-04-02
### Added
- [#8119: レース別出走表ページのデータをDBに格納する](https://redmine.u6k.me/issues/8119)
- [#8120: オッズ(単勝)ページのデータをDBに格納する](https://redmine.u6k.me/issues/8120)
- [#8121: レース結果ページのデータをDBに格納する](https://redmine.u6k.me/issues/8121)
- [#8122: 競走馬ページのデータをDBに格納する](https://redmine.u6k.me/issues/8122)
- [#8123: 騎手ページのデータをDBに格納する](https://redmine.u6k.me/issues/8123)
- [#8124: 調教師ページのデータをDBに格納する](https://redmine.u6k.me/issues/8124)

## [0.4.0] - 2020-03-30
### Added
- [#8110: 払戻金一覧ページをスクレイピングする](https://redmine.u6k.me/issues/8110)
- [#8111: レース別出走表ページをスクレイピングする](https://redmine.u6k.me/issues/8111)
- [#8112: オッズ(単勝)ページをスクレイピングする](https://redmine.u6k.me/issues/8112)
- [#8113: レース結果ページをスクレイピングする](https://redmine.u6k.me/issues/8113)
- [#8114: 競走馬ページをスクレイピングする](https://redmine.u6k.me/issues/8114)
- [#8115: 騎手ページをスクレイピングする](https://redmine.u6k.me/issues/8115)
- [#8116: 調教師ページをスクレイピングする](https://redmine.u6k.me/issues/8116)

## [0.3.0] - 2020-03-29
### Added
- [#8109: カレンダーページをスクレイピングする](https://redmine.u6k.me/issues/8109)

## [0.2.0] - 2020-03-29
### Added
- [#8117: ページ・キャッシュをS3に格納する](https://redmine.u6k.me/issues/8117)

## [0.1.0] - 2020-03-29
### Added
- [#8068: トップページのみ取得するScrapyアプリを構築、リリースする](https://redmine.u6k.me/issues/8068)
