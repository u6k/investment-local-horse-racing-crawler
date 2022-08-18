# 地方競馬データ・クローラー _(investment-local-horse-racing-crawler)_

[![Build Status](https://travis-ci.org/u6k/investment-local-horse-racing-crawler.svg?branch=master)](https://travis-ci.org/u6k/investment-local-horse-racing-crawler)
[![license](https://img.shields.io/github/license/u6k/investment-local-horse-racing-crawler.svg)](https://github.com/u6k/investment-local-horse-racing-crawler/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/u6k/investment-local-horse-racing-crawler.svg)](https://github.com/u6k/investment-local-horse-racing-crawler/releases)
[![WebSite](https://img.shields.io/website-up-down-green-red/https/shields.io.svg?label=u6k.Redmine)](https://redmine.u6k.me/projects/investment-local-horse-racing-crawler)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> 地方競馬予測に使用するデータを収集する

## Install

Dockerを使用します。

```bash
$ docker version
Client: Docker Engine - Community
 Version:           19.03.8
 API version:       1.40
 Go version:        go1.12.17
 Git commit:        afacb8b7f0
 Built:             Wed Mar 11 01:26:02 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.8
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.17
  Git commit:       afacb8b7f0
  Built:            Wed Mar 11 01:24:36 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.13
  GitCommit:        7ad184331fa3e55e52b890ea95e65ba581ae3429
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

`docker pull`します。

```bash
docker pull u6kapps/investment-local-horse-racing-crawler
```

前提

- PostgreSQL
- S3 (またはS3互換ストレージ)

コンポーネント構成、環境変数などは[docker-compose.yml](https://github.com/u6k/investment-local-horse-racing-crawler/blob/master/docker-compose.yml)を参照してください。

## Usage

クロールを開始する。

```bash
docker run u6kapps/investment-local-horse-racing-crawler scrapy crawl local_horse_racing
```

引数を指定してクロールする場合は、次のように実行する。

```bash
docker run u6kapps/investment-local-horse-racing-crawler scrapy crawl local_horse_racing -a start_url=https://xxx.com/xxx -a recache_race=true
```

ソースコードを構文チェック(Lint)する。

```bash
docker run u6kapps/investment-local-horse-racing-crawler flake8 .
```

ソースコードを整形する。

```bash
docker run u6kapps/investment-local-horse-racing-crawler isort .
```

```bash
docker run u6kapps/investment-local-horse-racing-crawler autopep8 -ivr .
```

スクレイピング機能をテストする。

```bash
docker run u6kapps/investment-local-horse-racing-crawler scrapy check local_horse_racing -L DEBUG
```

```bash
docker run u6kapps/investment-local-horse-racing-crawler pytest
```

## Other

最新情報は[Wiki](https://redmine.u6k.me/projects/investment-local-horse-racing-crawler/wiki/Wiki)をご覧ください。

## Maintainer

- u6k
  - [Twitter](https://twitter.com/u6k_yu1)
  - [GitHub](https://github.com/u6k)
  - [Blog](https://blog.u6k.me/)

## Contributing

当プロジェクトに興味を持っていただき、ありがとうございます。[既存のチケット](https://redmine.u6k.me/projects/investment-local-horse-racing-crawler/issues/)をご覧ください。

当プロジェクトは、[Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct)に準拠します。

## License

[MIT License](https://github.com/u6k/investment-local-horse-racing-crawler/blob/master/LICENSE)
