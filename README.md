### spider
- `link_spider.py` 爬取所有链接，在settings.py中设置年份，在target文件夹下新建相应年份的空文件夹，并复制放入code.txt
- `journal_spider.py` `boso_spider.py` `achievement_spider.py` 分别爬取settings.py中指定年份的期刊、博硕、成果的文章内容或Error中纪录的链接的文章内容
- `error_day_spider.py` 重新爬取失败日期的链接
- `error_page_spider` 重新爬取失败文章的内容 `error_page_loop_spider` 循环爬取失败的文章直到没有失败的文章
### util.py
工具类
### settings.py
- 年份设置
- 是否是爬取Error的链接内容
- 爬取速度设置
### middlewares.py
错误拦截处理
### pipelines.py
收集内容后的处理
### items.py
定义数据格式

### 配置执行环境
*由于使用scrapy框架多层嵌套循环导致效率低下，采用定时执行脚本的方式实现一年内自动化爬取，在Linux环境下使用定时执行工具cron每分钟执行脚本*
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
* * * * * sleep 20; /mnt/d/spider/zwData/keep-result.sh 2020 achievement >> /mnt/d/spider/zwData/keep-achievement.log 2>&1
```

**可根据target内的文件大小情况手动修改脚本中分割文件的方法**

```bash
# 一个类型一个文件，即achievement可都放在achievement.csv中
# result_filename=$result_type

# 一个大写字母为一个文件，即boso可分为boso_A.csv,boso_B.csv...
result_filename=${filename::-7}

# 直接以分类代码为一个文件，即journal可分为journal_A001.csv,journal_A002.csv..
# result_filename=${filename%.*}".csv"
```

