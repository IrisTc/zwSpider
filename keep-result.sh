#!/bin/bash
year=$1
result_type=$2
target_path="target/$year/"
result_path="result/$year/"
tensorcount=$(ps -ef | grep python3 | grep -v grep | wc -l)
cd /mnt/d/spider/zwData
if [ $tensorcount == 0 ]
then
	echo "scrapy is restart"
	files=$(ls $target_path)
	for filename in $files
	do
		if [[ $filename == $result_type* ]]
		then
			echo $filename
			break
		fi
	done
	if [[ $result_type == 'achievement' ]]
	then
		result_filename=$result_type
	elif [[ $result_type == 'boso' ]]
	then
		result_filename=${filename::-7}
	else
		result_filename=${filename%.*}
	fi
	echo "存储文件为$result_filename"
	python3 -m scrapy crawl $result_type -o "$result_path$result_filename.csv" -s LOG_FILE=warn.log
else
	echo "scrapy is running"
fi
