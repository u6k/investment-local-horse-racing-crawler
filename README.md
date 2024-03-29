# 地方競馬データ・クローラー _(investment-local-horse-racing-crawler)_

[![.github/workflows/build.yml](https://github.com/u6k/investment-local-horse-racing-crawler/actions/workflows/build.yml/badge.svg)](https://github.com/u6k/investment-local-horse-racing-crawler/actions/workflows/build.yml)
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
docker pull ghcr.io/u6k/local-horse-racing-crawler
```

## Usage

### クロール

クロールを開始する。

```bash
docker compose run app poe crawl -a start_url='https://xxx.example.com'
```

### 構文チェック、整形

ソースコードを構文チェック(Lint)する。

```bash
docker compose run app poe lint
```

ソースコードを整形する。

```bash
docker compose run app poe fix
```

### テスト

スクレイピング機能をテストする。

```bash
docker compose run app poe test
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
