#!/bin/bash -eu

tor &
sleep 120

privoxy /etc/privoxy/config &
sleep 10

scrapy crawl "$@"
