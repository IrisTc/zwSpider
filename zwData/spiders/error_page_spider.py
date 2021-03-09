import time

import requests
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

    name = "error-page"
    allowned_domains = ["kns.cnki.net"]

    # 爬取某年所有链接
    def start_requests(self):
        self.base_url = 'https://kns.cnki.net/kns/brief/brief.aspx?RecordsPerPage=50&QueryID=33&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&curpage='
        self.util = UtilClass(self.year)
        errorpage = self.util.getPage()
        for page in errorpage:
            print("[info]爬取errorpage" + page + '\n')
            params = page.split('&')
            code = params[0]
            date = params[1]
            pagenum = int(params[2])
            cookies = self.util.getCookies(date,code)
            url = self.base_url + str(pagenum)
            yield scrapy.Request(
                url=url,
                cookies=cookies,
                callback=self.parse_content,
                cb_kwargs={
                    'code': code,
                    'date': date,
                    'pagenum': pagenum
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
            print("[info]爬取%s %s 第%d页: %d个链接\n" % (code, date, pagenum, num))
            for row in rows:
                link = row.xpath('./td/a[@class="fz14"]/@href').extract_first()
                link_params = link.split('&')
                item = LinkItem()
                item['code'] = code
                item['url'] = link_params[3] + "&" + link_params[4] + "&" + link_params[5]
                item['db'] = row.xpath('./td')[5].xpath('./text()').extract_first().strip()
                yield item