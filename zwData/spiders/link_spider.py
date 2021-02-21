import datetime
import math
import re
import time

import requests
import scrapy

from zwData.items import LinkItem
from zwData.spiders.util import UtilClass


class LinkSpider(scrapy.Spider):
    name = 'link'
    allowed_domains = ['kns.cnki.net']

    def __init__(self, settings, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.year = settings.get('YEAR')
        self.base_url = 'https://kns.cnki.net/kns/brief/brief.aspx?RecordsPerPage=50&QueryID=33&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&curpage='

    # 获取setting中的年份值
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    # 重写startrequests
    def start_requests(self):
        util = UtilClass(self.year)
        dates = util.getAllDayPerYear()
        code = util.getCode()
        print("[info]开始爬取类别" + code)

        for date in dates:
            if date == datetime.datetime.now().strftime('%Y-%m-%d'): #若日期超过目前日期停止
                break
            cookies = self.getCookies(date,code)
            url_first = self.base_url + '1'
            yield scrapy.Request(
                url=url_first,
                cookies=cookies,
                callback=self.parse_page,
                cb_kwargs={
                    'cookies': cookies,
                    "code": code,
                    "date": date
                },
                dont_filter=True
            )

    def parse_page(self,response,cookies,code,date):
        cookies_now = cookies
        pagerTitleCell = response.xpath('//div[@class="pagerTitleCell"]/text()').extract_first()
        if pagerTitleCell == None:
            self.markError(code,date,0)
            return
        page = pagerTitleCell.strip()
        num = int(re.findall(r'\d+', page.replace(',', ''))[0]) # 文献数
        pagenum = math.ceil(num / 50)  #算出页数
        print("[info]%s %s 共有：%d篇文献, %d页" % (code,date,num,pagenum))
        if pagenum > 120:
            with open('target/' + self.year + '/overflow.txt', 'a') as f:
                f.write(date + code + '\n')
            return
        for i in range(1,pagenum+1):
            if i % 13 == 0:
                cookies_now = self.getCookies(date,code) # 超过15页换cookie
            url = self.base_url + str(i)
            yield scrapy.Request(
                url=url,
                cookies=cookies_now,
                callback=self.parse_content,
                cb_kwargs={
                    "pagenum": i,
                    "code": code,
                    "date": date
                },
                dont_filter=True
            )

    def parse_content(self,response,pagenum,code,date):
        rows = response.xpath('//table[@class="GridTableContent"]/tr')
        if len(rows) <= 1:
            self.markError(code,date,pagenum)
            return
        else:
            rows.pop(0) # 去掉标题行
            num = len(rows) # 该页链接数
            print("[info]爬取%s %s 第%d页: %d个链接" % (code,date,pagenum,num))
            for row in rows:
                link = row.xpath('./td/a[@class="fz14"]/@href').extract_first()
                link_params = link.split('&')
                item = LinkItem()
                item['code'] = code
                item['url'] = link_params[3] + "&" + link_params[4] + "&" + link_params[5]
                item['db'] = row.xpath('./td')[5].xpath('./text()').extract_first().strip()
                yield item


    def markError(self,code,date,pagenum):
        if pagenum == 0:
            with open('error/errorday.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '\n')
        else:
            with open('error/errorpage.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '&' + str(pagenum) + '\n')


    # 根据日期，分类代码获取cookies
    def getCookies(self, date, code):
        search_url = 'https://kns.cnki.net/kns/request/SearchHandler.ashx/'
        now_time = time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'
        params = {
            "action": "",
            "NaviCode": code,
            "ua": "1.21",
            "isinEn": "1",
            "PageName": "ASP.brief_result_aspx",
            "DbPrefix": "SCDB",
            "DbCatalog": "中国学术文献网络出版总库",
            "ConfigFile": "SCDB.xml",
            "db_opt": "CJFQ,CJRF,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,BDZK,CISD,SNAD,CCJD",
            "publishdate_from": date,
            "publishdate_to": date,
            "CKB_extension": "ZYW",
            "his": "0",
            '__': now_time
        }
        session_response = requests.get(search_url, params=params)
        cookies = requests.utils.dict_from_cookiejar(session_response.cookies)
        return cookies
