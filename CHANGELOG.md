# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- [#8825: タイムアウトエラーが多すぎる](https://redmine.u6k.me/issues/8825)

## [1.7.1] - 2020-11-03
### Fixed
- [#8819: 再キャッシュ・パラメーターが反映されていない](https://redmine.u6k.me/issues/8819)

## [1.7.0] - 2020-10-27
### Added
- [#8817: プロキシ経由でクロールできるようにする](https://redmine.u6k.me/issues/8817)

## [1.6.0] - 2020-10-24
### Added
- [#8778: 単勝・複勝以外のオッズもパースする](https://redmine.u6k.me/issues/8778)

### Changed
- [#8794: WebAPIではなくジョブとしてクロールを実行するようにする](https://redmine.u6k.me/issues/8794)
- [#8790: スクレイピング 処理で抽出した文字列をそのままDBに格納する](https://redmine.u6k.me/issues/8790)

### Removed
- [#8812: 不要なパラメーターを除去する](https://redmine.u6k.me/issues/8812)

## [1.5.0] - 2020-09-22
### Added
- [#8512: 着差を取得する](https://redmine.u6k.me/issues/8512)
- [#8554: 右・左回りを取得する](https://redmine.u6k.me/issues/8554)

## [1.4.0] - 2020-05-20
### Changed
- [#8285: 次のパース移譲は集約して行う](https://redmine.u6k.me/issues/8285)
- [#8416: Flaskについて、開発時は開発モードに設定する](https://redmine.u6k.me/issues/8416)
- [#8430: 引数を整理する](https://redmine.u6k.me/issues/8430)
- [#8419: 投票・清算ジョブのスケジューリングは、クローラーではなくジョブ管理側で行う](https://redmine.u6k.me/issues/8419)
- [#8410: 馬場状況を取得する](https://redmine.u6k.me/issues/8410)
- [#8407: 軽くテストする](https://redmine.u6k.me/issues/8407)
- [#8432: 上がり3ハロン取得する](https://redmine.u6k.me/issues/8432)

## [1.3.0] - 2020-05-05
### Added
- [#8341: 発走時刻の何分前に投票するか、何分後に結果確認するかを指定する](https://redmine.u6k.me/issues/8341)

## [1.2.1] - 2020-05-03
### Fixed
- [#8338: race_idの形式がページによって異なるため、同一レースを一意に識別できない](https://redmine.u6k.me/issues/8338)

## [1.2.0] - 2020-05-01
### Changed
- [#8263: Flaskアプリに変更して、ジョブ登録はFlaskで定義したWebAPIで受け付ける](https://redmine.u6k.me/issues/8263)
- [#8334: 当日のレース情報をクロールして、再クロール＆投票処理を予約する](https://redmine.u6k.me/issues/8334)

## [1.1.0] - 2020-04-18
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
