#!/bin/bash
year=$1
filename="target/$year/code.txt"
keepfile='keep-target.log'
timeout=20
tensorcount=$(ps -ef | grep python3 | grep -v grep | wc -l)
cd /mnt/d/spider/zwData
# 如果进程停止了则重新启动
if [ 0 == $tensorcount ];then
	echo "scrapy restart"
	python3 -m scrapy crawl link -s LOG_FILE=warn.log
# 如果进程仍在运行则通过输出日志查看是否超过timeout时间未响应
else
	echo "scrapy is running"
	infocount=$(tail -n $timeout $keepfile | grep info | grep -v grep | wc -l)
	runningcount=$(tail -n $timeout $keepfile | grep running | grep -v grep | wc -l)
	if [[ $infocount -eq 0 ]] && [[ $runningcount -ge 20 ]]
	then
		echo '超过' $timeout '分钟未响应'
		pid=$(ps -ef | grep python3 | grep -v grep | awk '{print $2}')
		# 杀死进程
		for item in $pid
		do
			echo -e "杀死进程$item \c"
			kill -9 $pid
		done

		# 将记录文件code.txt中的最后一个记录恢复 
		end=''
		while read line
		do
			if [[ $line == *_* ]]
			then
				end=$line
			fi
		done < $filename
		new=${end:1}
		echo -e "恢复code$end \c"
		sed -i "s/$end/$new/g" $filename

		# 删除最后一个记录的相关文件，防止数据重复
		echo -e "删除code$end相关文件\c"
		find "target/$year" -name "*$end.txt" | xargs rm -rf
		find 'error' -name "*$end.txt" | xargs rm -rf
	fi
fi

