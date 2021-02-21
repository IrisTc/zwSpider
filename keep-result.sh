#!/bin/bash
year=$1
result_type=$2
target_path="target/$year/"
result_path="result/$year/"
tensorcount=$(ps -ef | grep python3 | grep -v grep | wc -l)
cd /mnt/d/spider/zwData
if [ $tensorcount == 0 ]
then
	files=$(ls $target_path)
	for filename in $files
	do
		if [[ $filename == $result_type* ]]
		then
			echo $filename
			break
		fi
	done
	echo "scrapy restart"
	# result_filename=${filename%.*}".csv"
	python3 -m scrapy crawl $result_type -o "$result_path$result_type.csv"
else
	echo "scrapy is running"
fi
