#!/bin/bash
year=$1
target_path="author_output/"
result_path="author/$year/"
tensorcount=$(ps -ef | grep python3 | grep -v grep | wc -l)
cd /mnt/d/spider/zwData
if [ $tensorcount == 0 ]
then
	echo "scrapy is restart"
	files=$(ls $target_path)
	for filename in $files
	do
		if [[ $filename == author* ]]
		then
			echo $filename
			break
		fi
	done
	result_filename=${filename%.*}".csv"
	echo "存储文件为$result_filename"
	python3 -m scrapy crawl author -o "$result_path$result_filename" -s LOG_FILE=warn.log
else
	echo "scrapy is running"
fi
