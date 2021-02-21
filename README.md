##### 由于使用scrapy框架多层嵌套循环导致效率低下，采用定时执行脚本的方式实现一年内自动化爬取，在Linux环境下使用定时执行工具cron每分钟执行脚本
```
打开cron配置文件
crontab -e
```

##### 1.爬取所有链接
```
# 每隔一分钟执行keep-target.sh脚本 参数为年份 keep-target.log为输出日志
*/1 * * * * /mnt/d/spider/zwData/keep-target.sh 2020 > /mnt/d/spider/zwData/keep-target.log 2>&1
```

##### 2.爬取链接内容
```
# 爬取成果，每20秒执行keep-result.sh脚本 第一个参数为年份，第二个参数为爬取的类型
* * * * * sleep 20; /mnt/d/spider/zwData/keep-result.sh 2020 achievement > /mnt/d/spider/zwData/keep-achievement.log 2>&1
```

