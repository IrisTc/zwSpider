import math
import re
import scrapy

from zwData.items import LinkItem
from zwData.spiders.util import UtilClass

class JournalSpider(scrapy.Spider):
    def __init__(self, settings, *args, **kwargs):
        super(JournalSpider, self).__init__(*args, **kwargs)
        self.year = settings.get('YEAR')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    name = "error-day"
    allowned_domains = ["kns.cnki.net"]

    # 爬取某年所有链接
    def start_requests(self):
        self.base_url = 'https://kns.cnki.net/kns/brief/brief.aspx?RecordsPerPage=50&QueryID=33&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&curpage='
        self.util = UtilClass(self.year)
        errorday = self.util.getDay()
        for day in errorday:
            print("[info]爬取errorday" + day)
            params = day.split('&')
            code = params[0]
            date = params[1]
            cookies = self.util.getCookies(date,code)
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
            self.util.markError(code,date,0)
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
                cookies_now = self.util.getCookies(date,code) # 超过15页换cookie
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

    def parse_content(self, response, pagenum, code, date):
        rows = response.xpath('//table[@class="GridTableContent"]/tr')
        if len(rows) <= 1:
            self.util.markSecondError(code, date, pagenum)
            return
        else:
            rows.pop(0)  # 去掉标题行
            num = len(rows)  # 该页链接数
            print("[info]爬取%s %s 第%d页: %d个链接" % (code, date, pagenum, num))
            for row in rows:
                link = row.xpath('./td/a[@class="fz14"]/@href').extract_first()
                link_params = link.split('&')
                item = LinkItem()
                item['code'] = code
                item['url'] = link_params[3] + "&" + link_params[4] + "&" + link_params[5]
                item['db'] = row.xpath('./td')[5].xpath('./text()').extract_first().strip()
                yield item