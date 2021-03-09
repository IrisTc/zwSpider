#!/bin/bash
year=$1
name=$2
tensorcount=$(ps -ef | grep python3 | grep -v grep | wc -l)
cd /mnt/d/spider/zwData
if [ 0 == $tensorcount ];then
	echo "scrapy restart"
	python3 -m scrapy crawl $name -s LOG_FILE=warn.log
else
	echo "scrapy is running"
fi
