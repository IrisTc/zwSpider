#!/bin/bash
filename="keep.log"
time=6
infocount=$(tail -n $time $filename | grep info | grep -v grep | wc -l)
if [[ $infocount == 0 ]]
then
	echo '超过' $time '分钟未响应'
fi
infocount=1
runningcount=19
if [[ $infocount -eq 0 ]] && [[ $runningcount -ge 20 ]]
then
	echo 'ok'
fi
